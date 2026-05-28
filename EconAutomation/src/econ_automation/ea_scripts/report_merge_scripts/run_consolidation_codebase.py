from lxml import etree
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docxtpl import DocxTemplate
from copy import deepcopy

from docx.document import Document as DocxDocument
from docx.table import _Cell

def consolidate_runs_in_paragraph(paragraph):
    """
    Merge adjacent runs with identical rPr within a paragraph.
    Operates directly on the lxml element tree.
    """
    p = paragraph._p
    runs = p.findall(qn('w:r'))
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

        rpr_current = r_current.find(qn('w:rPr'))
        rpr_next = r_next.find(qn('w:rPr'))

        # Compare rPr serializations (None == None is fine too)
        def rpr_xml(rpr):
            return etree.tostring(rpr) if rpr is not None else b''

        if rpr_xml(rpr_current) == rpr_xml(rpr_next):
            # Merge: append all w:t (and w:br, w:tab) from next into current
            for child in list(r_next):
                if child.tag != qn('w:rPr'):
                    r_current.append(deepcopy(child))

            # Consolidate w:t elements — combine text, preserve xml:space
            t_elements = r_current.findall(qn('w:t'))
            if len(t_elements) > 1:
                combined = ''.join((t.text or '') for t in t_elements)
                for t in t_elements:
                    r_current.remove(t)
                new_t = OxmlElement('w:t')
                new_t.text = combined
                if combined != combined.strip():
                    new_t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                r_current.append(new_t)

            p.remove(r_next)
            runs = p.findall(qn('w:r'))  # refresh after mutation
        else:
            i += 1


def consolidate_all_runs(doc: DocxTemplate):
    """Apply run consolidation across all paragraphs and table cells."""

    docx = doc.docx  # the underlying python-docx Document

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
        for hf in (section.header, section.footer,
                   section.even_page_header, section.even_page_footer,
                   section.first_page_header, section.first_page_footer):
            if hf and not hf.is_linked_to_previous:
                process_paragraphs(hf)