import logging
from dataclasses import dataclass, field, is_dataclass, fields
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


@dataclass
class PVEarningsToggles:
    """
    GUI-sourced toggle values for the PV Earnings report template.
    Passed from the GUI layer into PVEarningsContextBuilder to override
    dataclass inference.  All fields default to a conservative "off" state
    so a partially-constructed instance is safe to use.
    """

    base1_toggle: bool = True
    base2_toggle: bool = False
    base3_toggle: bool = False
    credit1_toggle: bool = False
    credit2_toggle: bool = False
    credit3_toggle: bool = False
    meals_toggle: bool = False
    benefits_toggle: bool = False
    taxed_toggle: bool = False
    projection_type_toggle: str = "WLE"  # "WLE" or "toage"
    rehab_report_types: list[str] = field(default_factory=list)  # e.g. ["LCP", "Voc"]


class PVEarningsContextBuilder:
    """
    Builds the Jinja2 render context for PV_Earnings_Report_Template.

    All toggle flags and derived values that drive the template's conditional
    logic live here — not in the template itself.  Add new one-off business
    rules as named helper methods (prefix ``_``) so the logic stays readable
    and testable without opening Word.

    Usage::

        ctx = PVEarningsContextBuilder(ea_main_dataclass, gui_toggles).build()

    When ``gui_toggles`` is provided the toggle values come directly from the
    GUI (checkboxes / comboboxes).  When omitted the builder falls back to
    inferring toggles from the extracted dataclass — used by the test harness
    and any headless / scripted invocation.
    """

    def __init__(
        self, ea_main_dataclass: Any, gui_toggles: PVEarningsToggles | None = None
    ) -> None:
        self._raw = ea_main_dataclass
        self._gui = gui_toggles

    # ── Public API ────────────────────────────────────────────────────────

    def build(self) -> dict[str, Any]:
        ctx: dict[str, Any] = {}
        ctx.update(self._all_fields())
        ctx.update(self._toggles())
        ctx.update(self._rehab_report_types())
        ctx.update(self._derived_fields())
        ctx.update(self._aliases())
        return ctx

    # ── Private helpers ───────────────────────────────────────────────────

    def _get(self, name: str, default: Any = None) -> Any:
        return getattr(self._raw, name, default)

    def _is_populated(self, name: str) -> bool:
        """True when a field has a non-empty, non-zero value after formatting."""
        val = self._get(name)
        if val is None:
            return False
        if isinstance(val, str):
            # Treat formatted zero-currency/zero-percent strings as absent
            return bool(val.strip()) and val.strip() not in ("$0", "0", "0.00", "0.00%")
        if isinstance(val, (int, float)):
            return val != 0
        return bool(val)

    def _all_fields(self) -> dict[str, Any]:
        """
        Pass through every extracted field from the flattened dataclass.
        Includes non-primitive types (RichText, image objects) so docxtpl
        can render {{r ...}} tags correctly.
        """
        if isinstance(self._raw, BaseModel):
            return {
                k: v for k, v in self._raw.__dict__.items() if not k.startswith("_")
            }
        if is_dataclass(self._raw):
            return {f.name: self._get(f.name) for f in fields(self._raw)}
        # Fallback: plain object with __dict__
        return {k: v for k, v in vars(self._raw).items() if not k.startswith("_")}

    def _toggles(self) -> dict[str, Any]:
        """
        Return all boolean/string flags that drive template conditionals.

        When a PVEarningsToggles instance was supplied at construction time
        (i.e. the GUI is in use) those values are used directly.  Otherwise
        toggles are inferred from the extracted dataclass — used by the test
        harness and headless runs.

        projection_type_toggle:
            'WLE'   — work-life equivalent (standard)
            'toage' — to-age projection (used when WLE is inappropriate)
        """
        if self._gui is not None:
            return {
                "base1_toggle": self._gui.base1_toggle,
                "base2_toggle": self._gui.base2_toggle,
                "base3_toggle": self._gui.base3_toggle,
                "projection_type_toggle": self._gui.projection_type_toggle,
                "credit1_toggle": self._gui.credit1_toggle,
                "credit2_toggle": self._gui.credit2_toggle,
                "credit3_toggle": self._gui.credit3_toggle,
                "meals_toggle": self._gui.meals_toggle,
                "benefits_toggle": self._gui.benefits_toggle,
                "taxed_toggle": self._gui.taxed_toggle,
            }

        # Fallback: infer from extracted dataclass values
        return {
            "base1_toggle": self._is_populated("b1e_WLE_earnings"),
            "base2_toggle": self._is_populated("b2e_WLE_earnings"),
            "base3_toggle": self._is_populated("b3e_WLE_earnings"),
            "projection_type_toggle": "WLE",
            "credit1_toggle": self._is_populated("credit1_WLE_earnings"),
            "credit2_toggle": self._is_populated("credit2_WLE_earnings"),
            "credit3_toggle": self._is_populated("credit3_WLE_earnings"),
            "meals_toggle": self._is_populated("b1e_WLE_pretrial_meals_adj"),
            "benefits_toggle": self._is_populated("b1e_WLE_pretrial_benefits_adj"),
            "taxed_toggle": self._is_populated("eff_tax_rate"),
        }

    def _rehab_report_types(self) -> dict[str, Any]:
        """
        Builds the ``rehab_report_types`` list consumed by:
            {% if 'LCP' in rehab_report_types %}
            {% if 'MCP' in rehab_report_types %}
            {% if 'Voc' in rehab_report_types %}

        When GUI toggles are present the list comes directly from them.
        Otherwise the list is inferred from the extracted dataclass.
        """
        if self._gui is not None:
            return {"rehab_report_types": list(self._gui.rehab_report_types)}

        # Fallback: infer from extracted dataclass values
        types: list[str] = []
        if self._is_populated("rehab_expert_name_full_with_titles"):
            types.append("LCP")
        if self._is_populated("MCP_expert_name_full_with_titles"):
            types.append("MCP")
        # if self._is_populated("Voc_expert_name_full_with_titles"):
        #     types.append("Voc")
        return {"rehab_report_types": types}

    def _rehab_report_names(self, rehab_report_types: list[str]) -> list[str]:
        """
        Returns a list of rehab report proper names (i.e. "Life Care Plan", "Medical Cost Projection").
        """
        names_map = {
            "LCP": "Life Care Plan",
            "MCP": "Medical Cost Projection",
            "Voc": "Vocational Opinion",
        }
        return [names_map[r] for r in rehab_report_types]

    def _aliases(self) -> dict[str, Any]:
        """
        Resolves known variable-name inconsistencies between the template
        and the extracted dataclass.  Each entry here documents the mismatch
        so it can be cleaned up in the template when convenient.
        """
        return {
            # Technical Summary table uses 'clm_WLE_from_trial_full';
            # all other template references use 'claimant_WLE_from_trial_full'.
            # Remove this alias once the template is corrected to use one name.
            "clm_WLE_from_trial_full": self._get("claimant_WLE_from_trial_full"),
        }

    def _derived_fields(self) -> dict[str, Any]:
        """
        Compute derived values that are not directly present in the
        extracted dataclass. Used in conjunction with conditionals within
        the Word template.
        """
        toggles = self._toggles()
        return {
            # Maps projection_type_toggle → the string the template checks against.
            # GUI stores "toage"; template was authored against "TR".
            "earnings_projection_type": "WLE"
            if toggles["projection_type_toggle"] == "WLE"
            else "TR",
            # This template is always the PV Earnings report; the outer {%p if %} wrapper
            # in the template checks 'PV Earnings' in report_templates.
            "report_templates": ["PV Earnings"],
            "single_base": (
                True
                if toggles["base1_toggle"]
                and not toggles["base2_toggle"]
                and not toggles["base3_toggle"]
                else False
            ),
            "single_credit": (
                True
                if toggles["credit1_toggle"]
                and not toggles["credit2_toggle"]
                and not toggles["credit3_toggle"]
                else False
            ),
            "growth_rate_projection": (
                "SSA"
                if (
                    (
                        toggles["projection_type_toggle"] == "WLE"
                        and int(self._get("claimant_WLE_from_trial_int")) >= 11
                    )
                    or (
                        toggles["projection_type_toggle"] == "toage"
                        and int(self._get("claimant_retire_from_trial_int")) >= 11
                    )
                )
                else "CBO"
            ),
        }


def build_pv_earnings_context(
    ea_main_dataclass: Any,
    gui_toggles: PVEarningsToggles | None = None,
) -> dict[str, Any]:
    """Module-level entry point for merge_reports_core dispatch."""
    return PVEarningsContextBuilder(ea_main_dataclass, gui_toggles).build()
