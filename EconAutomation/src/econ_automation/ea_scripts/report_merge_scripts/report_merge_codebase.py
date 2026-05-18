import logging
from pathlib import Path
from typing import Any
from datetime import datetime, date

from docxtpl import DocxTemplate

logger = logging.getLogger(__name__)


def determine_variable_map(ea_main_dataclass: Any) -> dict[str, Any]:
    """
    Builds the Jinja2 render context from the ea_main_dataclass.
    Keys are plain variable names matching {{ variable_name }} tokens in templates.
    """
    variable_map = ea_main_dataclass.__dict__

    try:
        # Filter out any non-string or non-numeric values to prevent docxtpl errors
        variable_map = {
            k: v
            for k, v in variable_map.items()
            if isinstance(
                v,
                (
                    str,
                    int,
                    float,
                    datetime,
                    date,
                ),
            )
        }
    except TypeError:
        logger.exception("determine_variable_map() TypeError")
        raise

    return variable_map


def save_output_document(
    doc: DocxTemplate,
    variable_map: dict[str, Any],
    report_type: str,
    selected_output_filepaths: list[Path],
) -> None:
    """
    Saves the rendered DocxTemplate to each output filepath.
    """
    try:
        for output_filepath in selected_output_filepaths:
            base_stem = (
                f"{variable_map['claimant_name_last']}"
                f"{variable_map['claimant_name_first_initial']}"
                f" - {report_type}"
            )
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
        for template_filepath in selected_template_filepaths:
            doc = DocxTemplate(str(template_filepath))
            doc.render(variable_map)
            save_output_document(
                doc=doc,
                variable_map=variable_map,
                report_type=template_filepath.stem,
                selected_output_filepaths=selected_output_filepaths,
            )
    except Exception as e:
        logger.exception(f"Error autofilling Word document templates: {e}")
        raise
