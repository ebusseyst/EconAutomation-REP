import logging
from pathlib import Path
from typing import Any
from datetime import datetime, date

from docxtpl import DocxTemplate
from jinja2 import Environment, Undefined

logger = logging.getLogger(__name__)


class _DebugUndefined(Undefined):
    """Renders as [[ variable_name ]] so missing template variables are visible in output."""
    __slots__ = ()

    def __str__(self) -> str:
        return f"[[ {self._undefined_name} ]]"


def determine_variable_map(ea_main_dataclass: Any) -> dict[str, Any]:
    """
    Builds the Jinja2 render context from the ea_main_dataclass.
    Keys are plain variable names matching {{ variable_name }} tokens in templates.
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
            name_first_initial = dir_name.split(",")[1].strip()[0] if "," in dir_name else ""
            base_stem = f"{name_last}{name_first_initial} - {report_type}"
            final_output_path = output_filepath / f"{base_stem}.docx"

            output_filepath.mkdir(parents=True, exist_ok=True)

            counter = 0
            while final_output_path.exists():
                counter += 1
                final_output_path = output_filepath / f"{base_stem}({counter}).docx"

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
) -> None:
    """
    Renders all Word document templates via docxtpl and saves the outputs.
    Templates must use Jinja2 syntax: {{ variable_name }}.
    """
    variable_map = determine_variable_map(ea_main_dataclass)

    try:
        jinja_env = Environment(undefined=_DebugUndefined)
        for template_filepath in selected_template_filepaths:
            doc = DocxTemplate(str(template_filepath))
            doc.render(variable_map, jinja_env=jinja_env)
            save_output_document(
                doc=doc,
                report_type=template_filepath.stem,
                selected_output_filepaths=selected_output_filepaths,
            )
    except Exception as e:
        logger.exception(f"Error autofilling Word document templates: {e}")
        raise
