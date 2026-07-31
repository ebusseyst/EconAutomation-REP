import logging
from pathlib import Path
from typing import Any
from datetime import datetime, date

from docx.shared import Mm

from docxtpl import DocxTemplate, InlineImage
from jinja2 import Environment, Undefined, TemplateSyntaxError

from econ_automation.ea_scripts.report_merge_scripts.run_consolidation_codebase import (
    consolidate_all_runs,
    remove_empty_numbered_paragraphs,
)
from econ_automation.ea_scripts.report_merge_scripts.pv_earnings_context_codebase import (
    build_pv_earnings_context,
)
from econ_automation.ea_scripts.report_merge_scripts.pvlcp_context_codebase import (
    build_pvlcp_context,
)

logger = logging.getLogger(__name__)

# Maps template stem → context-builder function.
# Each builder has signature: (ea_main_dataclass, gui_toggles=None) -> dict.
# Add an entry here whenever a new template gets its own context builder.
_CONTEXT_BUILDERS: dict[str, Any] = {
    "PV_Earnings_Report_Template": build_pv_earnings_context,
    "PVLCP_Report_Template": build_pvlcp_context,
}


class _DebugUndefined(Undefined):
    """Renders as [[ variable_name ]] so missing template variables are visible in output."""

    __slots__ = ()

    def __str__(self) -> str:
        return f"[[ {self._undefined_name} ]]"


def determine_variable_map(ea_main_dataclass: Any) -> dict[str, Any]:
    """
    Fallback context builder: passes all primitive fields through as-is.
    Non-primitive values are replaced with [[ key ]] so they appear visibly
    in output rather than crashing the render.
    """
    try:
        variable_map = {
            k: (v if isinstance(v, (str, int, float, datetime, date)) else f"[[ {k} ]]")
            for k, v in ea_main_dataclass.__dict__.items()
        }
    except TypeError:
        logger.exception("determine_variable_map() TypeError")
        raise

    return variable_map


def save_output_document(
    doc: DocxTemplate,
    report_type: str,
    selected_output_filepaths: list[Path],
) -> None:
    """
    Saves the rendered DocxTemplate to each output filepath.
    """
    try:
        for output_filepath in selected_output_filepaths:
            dir_name = output_filepath.name  # e.g. "Gaston, Casper (J. D'Attorney)"
            name_last = dir_name.split(",")[0].strip() if "," in dir_name else dir_name
            name_first_initial = (
                dir_name.split(",")[1].strip()[0] if "," in dir_name else ""
            )
            base_stem = f"{name_last}{name_first_initial} - {report_type}"
            output_dir = output_filepath / "Reports and Invoices"
            output_dir.mkdir(parents=True, exist_ok=True)
            final_output_path = output_dir / f"{base_stem}.docx"

            counter = 0
            while final_output_path.exists():
                counter += 1
                final_output_path = output_dir / f"{base_stem}({counter}).docx"

            doc.save(str(final_output_path))
            logger.info(f"Saved output document to: {final_output_path}")

    except KeyError:
        logger.exception("save_output_document() KeyError")
        raise
    except TypeError:
        logger.exception("save_output_document() TypeError")
        raise
    except FileNotFoundError:
        logger.exception("save_output_document() FileNotFoundError")
        raise
    except Exception as e:
        logger.exception(f"save_output_document() error: {e}")
        raise


def merge_reports_core(
    ea_main_dataclass: Any,
    selected_template_filepaths: list[Path],
    selected_output_filepaths: list[Path],
    gui_overrides: dict[str, Any] | None = None,
    image_paths: dict[str, Path] | None = None,
) -> None:
    """
    Renders all Word document templates via docxtpl and saves the outputs.
    Templates must use docxtpl/Jinja2 syntax: {{ variable_name }}.

    Per-template context builders are dispatched via _CONTEXT_BUILDERS; any
    template without an entry falls back to determine_variable_map().
    Run consolidation is applied to every loaded template before rendering to
    repair any same-rPr tag splits introduced by Word editing.

    ``gui_overrides`` maps template stem → PVEarningsToggles.  When an entry
    is present for a template, its toggles are forwarded to the context
    builder so GUI widget state drives the report rather than dataclass
    inference.

    ``image_paths`` maps template variable name → Path for chart/table images
    extracted from workbooks. Each path is converted to an InlineImage bound
    to the current DocxTemplate before rendering.
    """
    jinja_env = Environment(undefined=_DebugUndefined)
    for template_filepath in selected_template_filepaths:
        doc: DocxTemplate | None = None
        try:
            builder = _CONTEXT_BUILDERS.get(template_filepath.stem)
            if builder is not None:
                toggles = (gui_overrides or {}).get(template_filepath.stem)
                context = builder(ea_main_dataclass, toggles)
                logger.info(
                    f"merge_reports_core: using context builder for {template_filepath.stem}"
                )
            else:
                context = determine_variable_map(ea_main_dataclass)
                logger.info(
                    f"merge_reports_core: using fallback variable map for {template_filepath.stem}"
                )

            doc = DocxTemplate(str(template_filepath))

            if image_paths:
                for var_name, img_path in image_paths.items():
                    if img_path.exists():
                        context[var_name] = InlineImage(
                            doc, str(img_path), width=Mm(150)
                        )
                    else:
                        logger.warning(
                            f"merge_reports_core: image not found, skipping '{var_name}': {img_path}"
                        )

            consolidate_all_runs(doc)
            doc.render(context, jinja_env=jinja_env)
            n = remove_empty_numbered_paragraphs(doc.docx)
            if n:
                logger.info(
                    "merge_reports_core: removed %d empty numbered paragraph(s) from %s",
                    n,
                    template_filepath.name,
                )
            report_type = template_filepath.stem.removesuffix("_Template").replace(
                "_", " "
            )
            save_output_document(
                doc=doc,
                report_type=report_type,
                selected_output_filepaths=selected_output_filepaths,
            )
        except TemplateSyntaxError as e:
            # Dump the post-consolidation XML so the split tag can be located.
            try:
                import tempfile

                if doc is not None:
                    # pyrefly: ignore [missing-attribute]
                    xml_bytes = doc.get_docx()._part.blob
                    dump_path = (
                        Path(tempfile.gettempdir())
                        / f"_debug_{template_filepath.stem}.xml"
                    )
                    dump_path.write_bytes(xml_bytes)
                    logger.error(
                        "TemplateSyntaxError: post-consolidation XML written to %s — "
                        "search for 'endif' in that file to locate the unmatched tag.",
                        dump_path,
                    )
            except Exception:
                pass
            logger.error(
                "TemplateSyntaxError in '%s' at XML line %s: %s — "
                "likely cause: Word split a Jinja2 tag (e.g. {%% if %%} or {%% endif %%}) "
                "across XML runs with differing w:rPr or w:proofErr markers. "
                "Open the template in Word, select the affected tag text, clear all "
                "character formatting (Ctrl+Space), and re-save.",
                template_filepath.name,
                getattr(e, "lineno", "?"),
                e,
            )
            raise
        except Exception as e:
            logger.exception(
                f"Error rendering template '{template_filepath.name}': {e}"
            )
            raise
