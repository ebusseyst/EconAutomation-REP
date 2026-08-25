import logging
from dataclasses import dataclass, field, fields, is_dataclass
from typing import Any

from docxtpl import RichText
from pydantic import BaseModel

logger = logging.getLogger(__name__)

_CPI_CATEGORIES = [
    "physer",
    "othmedpro",
    "medcarser",
    "predru",
    "nonpredru",
    "allite",
    "hosser",
    "inpser",
    "outser",
    "medequ",
]


@dataclass
class PVLCPToggles:
    """
    GUI-sourced toggle values for the PVLCP_Report_Template.
    The only conditional logic in the PVLCP template is which rehab report
    type(s) are present: 'LCP' (Life Care Plan) and/or 'MCP' (Medical Cost
    Projection).  This is driven by the Reference Type combobox in the GUI.
    """

    rehab_report_types: list[str] = field(default_factory=lambda: ["LCP"])


class PVLCPContextBuilder:
    """
    Builds the Jinja2 render context for PVLCP_Report_Template.

    Usage::

        ctx = PVLCPContextBuilder(ea_main_dataclass, gui_toggles).build()

    When ``gui_toggles`` is provided the rehab_report_types list comes
    directly from the GUI (Reference Type combobox).  When omitted the
    builder falls back to inferring the list from the extracted dataclass
    — used by the test harness and headless runs.
    """

    def __init__(
        self, ea_main_dataclass: Any, gui_toggles: PVLCPToggles | None = None
    ) -> None:
        self._raw = ea_main_dataclass
        self._gui = gui_toggles

    # ── Public API ────────────────────────────────────────────────────────

    def build(self) -> dict[str, Any]:
        ctx: dict[str, Any] = {}
        ctx.update(self._all_fields())
        ctx.update(self._rehab_report_types())
        ctx.update(self._cpi_derived_fields())
        return ctx

    # ── Private helpers ───────────────────────────────────────────────────

    def _get(self, name: str, default: Any = None) -> Any:
        return getattr(self._raw, name, default)

    def _is_populated(self, name: str) -> bool:
        val = self._get(name)
        if val is None:
            return False
        if isinstance(val, str):
            return bool(val.strip()) and val.strip() not in ("$0", "0", "0.00", "0.00%")
        if isinstance(val, (int, float)):
            return val != 0
        return bool(val)

    def _all_fields(self) -> dict[str, Any]:
        if isinstance(self._raw, BaseModel):
            return {
                k: v for k, v in self._raw.__dict__.items() if not k.startswith("_")
            }
        if is_dataclass(self._raw):
            return {f.name: self._get(f.name) for f in fields(self._raw)}
        return {k: v for k, v in vars(self._raw).items() if not k.startswith("_")}

    def _rehab_report_types(self) -> dict[str, Any]:
        """
        Builds the ``rehab_report_types`` list consumed by:
            {% if 'LCP' in rehab_report_types %}
            {% if 'MCP' in rehab_report_types %}

        When GUI toggles are present the list comes directly from them
        (driven by the Reference Type combobox).  Otherwise inferred
        from the extracted dataclass.
        """
        if self._gui is not None:
            return {"rehab_report_types": list(self._gui.rehab_report_types)}

        # Fallback: infer from extracted dataclass values
        types: list[str] = []
        if self._is_populated("rehab_expert_name_full_with_titles"):
            types.append("LCP")
        # if self._is_populated("MCP_expert_name_full_with_titles"):
        #     types.append("MCP")
        return {"rehab_report_types": types}

    def _cpi_derived_fields(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for cat in _CPI_CATEGORIES:
            has_low = self._is_populated(f"WC_CPI_selcat_{cat}low")
            has_high = self._is_populated(f"WC_CPI_selcat_{cat}high")

            out[f"WC_CPI_selcat_{cat}"] = has_low or has_high

            # Pulls unmodified percentage (type: str) 
            low_val_orig = self._get(f"WC_CPI_selcat_{cat}low_growth_rate") or ""
            high_val_orig = self._get(f"WC_CPI_selcat_{cat}high_growth_rate") or ""

            # Enforcing CPI growth rate-only one significant figure only policy (08/25/2026)
            def split_CPI_growth_rate(orig_val) :
                delim = "."

                val_before, val_after = orig_val.split(delim) if orig_val else ""
                val_after = val_after[0]
                
                return f"{val_before}.{val_after}%"
            
            
            low_val = split_CPI_growth_rate(low_val_orig) if low_val_orig else ""
            high_val = split_CPI_growth_rate(high_val_orig) if high_val_orig else ""

            rt = RichText()
            if has_low and has_high:
                rt.add(low_val, font="Times New Roman", size=24)
                rt.xml += "<w:r><w:br/></w:r><w:r><w:br/></w:r>"
                rt.add(high_val, font="Times New Roman", size=24)
            elif has_low:
                rt.add(low_val, font="Times New Roman", size=24)
            elif has_high:
                rt.add(high_val, font="Times New Roman", size=24)
            out[f"WC_CPI_selcat_{cat}_growth_rates"] = rt

        return out

    def _derived_fields(self) -> dict[str, Any]:
        """
        Compute derived values that are not directly present in the
        extracted dataclass. Used in conjunction with conditionals within
        the Word template.
        """
        return {
            "report_templates": ["PVLCP"],
            "PV_is_range": sum(
                self._is_populated(f)
                for f in (
                    "PV_Summary_No_Rounding_Total_Low",
                    "PV_Summary_No_Rounding_Total_Mid",
                    "PV_Summary_No_Rounding_Total_High",
                )
            )
            >= 2,
        }

def build_pvlcp_context(
    ea_main_dataclass: Any,
    gui_toggles: PVLCPToggles | None = None,
) -> dict[str, Any]:
    """Module-level entry point for merge_reports_core dispatch."""
    return PVLCPContextBuilder(ea_main_dataclass, gui_toggles).build()
