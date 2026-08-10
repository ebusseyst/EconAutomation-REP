import re as _re
from copy import deepcopy

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docxtpl import DocxTemplate
from lxml import etree

# Word automatically injects these properties without user intent.
# Stripping them before comparison lets adjacent runs that are visually
# identical (but tagged with different language/proofing annotations) merge,
# which prevents Jinja2 tags from being split across XML runs.
_AUTO_INSERTED_PROPS = frozenset([qn("w:lang"), qn("w:noProof")])

# Inline paragraph elements that Word injects as spell/grammar-check markers.
# They have no semantic content but sit between runs as sibling elements,
# causing the adjacency check to treat neighboring runs as non-adjacent.
# Stripping them before consolidation allows the runs to merge correctly.
_TRANSPARENT_PARA_TAGS = frozenset([qn("w:proofErr")])


def _normalize_rpr(rpr) -> bytes:
    """
    Return a normalized serialization of a run-properties element.
    Auto-inserted Word properties (w:lang, w:noProof) are stripped so they
    don't prevent otherwise-identical runs from merging.
    An rPr reduced to empty is treated the same as no rPr (returns b"").
    """
    if rpr is None:
        return b""
    rpr_copy = deepcopy(rpr)
    for tag in _AUTO_INSERTED_PROPS:
        for elem in rpr_copy.findall(tag):
            rpr_copy.remove(elem)
    return etree.tostring(rpr_copy) if len(rpr_copy) > 0 else b""


def _strip_transparent_elements(p) -> None:
    """Remove proofErr markers (and similar) that sit between runs as siblings."""
    for tag in _TRANSPARENT_PARA_TAGS:
        for elem in p.findall(tag):
            p.remove(elem)


def consolidate_runs_in_paragraph(paragraph):
    """
    Merge adjacent runs with equivalent rPr within a paragraph.
    Operates directly on the lxml element tree.
    """
    p = paragraph._p
    _strip_transparent_elements(p)
    runs = p.findall(qn("w:r"))
    if len(runs) < 2:
        return

    i = 0
    while i < len(runs) - 1:
        r_current = runs[i]
        r_next = runs[i + 1]

        # Check that they're actually adjacent siblings (no intervening elements)
        current_idx = list(p).index(r_current)
        next_idx = list(p).index(r_next)
        if next_idx != current_idx + 1:
            i += 1
            continue

        rpr_current = r_current.find(qn("w:rPr"))
        rpr_next = r_next.find(qn("w:rPr"))

        if _normalize_rpr(rpr_current) == _normalize_rpr(rpr_next):
            # Merge: append all w:t (and w:br, w:tab) from next into current
            for child in list(r_next):
                if child.tag != qn("w:rPr"):
                    r_current.append(deepcopy(child))

            # Consolidate w:t elements — combine text, preserve xml:space
            t_elements = r_current.findall(qn("w:t"))
            if len(t_elements) > 1:
                combined = "".join((t.text or "") for t in t_elements)
                for t in t_elements:
                    r_current.remove(t)
                new_t = OxmlElement("w:t")
                new_t.text = combined
                if combined != combined.strip():
                    new_t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                r_current.append(new_t)

            p.remove(r_next)
            runs = p.findall(qn("w:r"))  # refresh after mutation
        else:
            i += 1


def fix_same_row_tr_tags(doc: DocxTemplate) -> None:
    """
    Restructure table rows where {%tr if...%} and {%tr endif%} appear in the
    SAME <w:tr> element.

    docxtpl's patch_xml regex is greedy and replaces the ENTIRE <w:tr> with
    whichever {%tr...%} tag it matches last — always the endif — discarding the
    opening if condition. The standard docxtpl contract requires each tag to be
    in its own dedicated row. This function enforces that contract automatically:

      Before:  <w:tr> {%tr if cond%} ...data... {%tr endif%} </w:tr>
      After:   <w:tr> {%tr if cond%} </w:tr>
               <w:tr> ...data...                </w:tr>
               <w:tr> {%tr endif%}              </w:tr>

    Must be called AFTER run consolidation so the tags are guaranteed to be in
    complete, single <w:t> elements.
    """
    _docx = doc.get_docx()
    if _docx is None:
        return
    body = _docx._element.body

    # Collect first — modifying the tree while iterating is unsafe.
    rows_to_fix: list[tuple] = []
    for tr in body.iter(qn("w:tr")):
        all_text = "".join(t.text or "" for t in tr.iter(qn("w:t")))
        if_m = _re.search(r"\{%tr if ([^%]+)%\}", all_text)
        endif_m = _re.search(r"\{%tr endif\s*%\}", all_text)
        if if_m and endif_m:
            rows_to_fix.append((tr, if_m.group(1).strip()))

    for tr, condition in rows_to_fix:
        parent = tr.getparent()
        if parent is None:
            continue

        # Strip {%tr ...%} tags from text elements so the data row is clean.
        for t in tr.iter(qn("w:t")):
            if t.text:
                t.text = _re.sub(r"\{%tr if[^%]+%\}", "", t.text)
                t.text = _re.sub(r"\{%tr endif\s*%\}", "", t.text)

        idx = list(parent).index(tr)

        def _make_tag_row(tag_text: str):
            row = OxmlElement("w:tr")
            tc = OxmlElement("w:tc")
            p = OxmlElement("w:p")
            r = OxmlElement("w:r")
            t = OxmlElement("w:t")
            t.text = tag_text
            r.append(t)
            p.append(r)
            tc.append(p)
            row.append(tc)
            return row

        parent.insert(idx, _make_tag_row(f"{{%tr if {condition} %}}"))
        # tr is now at idx+1; insert endif after it
        parent.insert(idx + 2, _make_tag_row("{%tr endif %}"))


def remove_empty_numbered_paragraphs(document) -> int:
    """
    Remove auto-numbered paragraphs that have no text after rendering.

    Inline {% if condition %}text{% endif %} blocks leave the enclosing <w:p>
    element intact when condition is False — only the text is removed — which
    produces a blank numbered line. This sweeps those residual paragraphs out
    of the rendered document before saving.

    Returns the count of paragraphs removed.
    """
    body = document.element.body
    to_remove = []
    for para in body.iter(qn("w:p")):
        ppr = para.find(qn("w:pPr"))
        if ppr is None:
            continue
        if ppr.find(qn("w:numPr")) is None:
            continue
        text = "".join((t.text or "") for t in para.iter(qn("w:t"))).strip()
        if not text:
            to_remove.append(para)
    for para in to_remove:
        para.getparent().remove(para)
    return len(to_remove)


def consolidate_all_runs(doc: DocxTemplate):
    """Apply run consolidation across all paragraphs and table cells."""

    docx = doc.get_docx()  # loads lazily via init_docx() in docxtpl 0.20+

    def process_paragraphs(container):
        for para in container.paragraphs:
            consolidate_runs_in_paragraph(para)
        for table in container.tables:
            for row in table.rows:
                for cell in row.cells:
                    process_paragraphs(cell)

    process_paragraphs(docx)
    # Also handle headers/footers
    # pyrefly: ignore [missing-attribute]
    for section in docx.sections:
        for hf in (
            section.header,
            section.footer,
            section.even_page_header,
            section.even_page_footer,
            section.first_page_header,
            section.first_page_footer,
        ):
            if hf and not hf.is_linked_to_previous:
                process_paragraphs(hf)

    # Fix same-row {%tr if/endif%} patterns after run consolidation has ensured
    # the tags are in complete, single <w:t> elements.
    fix_same_row_tr_tags(doc)
