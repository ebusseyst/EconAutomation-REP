import logging
from dataclasses import dataclass, field, is_dataclass, fields
from typing import Any
import re

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

class Base:
    """
    Represents a single base earnings variable in the report.
    """
    def __init__(self, base_stem: str, ):
        self._base_stem = base_stem
        self._suffixes = [
            "_earnings",
            "_eff_tax_rate",
            "_growth_rate",
            "_pretrial_loss_notax",
            "_pretrial_loss_taxed",
            "_posttrial_loss_notax",
            "_posttrial_loss_taxed",
            "_total_loss_notax",
            "_total_loss_taxed",
        ]

    def build(self):
        for suffix in self._suffixes:
            variable = f"{self._base_stem}{suffix}"
            self.__dict__[variable] = self._get(variable)

class BaseBuilder:
    """
    Builds the attributes for each base earnings variable in the report.
    """

    def __init__(
        self,
        ea_main_dataclass: Any,
        pv_earnings_toggles: PVEarningsToggles,
        base_stem: str,
    ) -> None:
        self._raw = ea_main_dataclass
        self._pv_earnings_toggles = pv_earnings_toggles
        self._base_stem = base_stem

    suffixes = [
        "_earnings",
        "_eff_tax_rate",
        "_growth_rate",
        "_pretrial_loss_notax",
        "_pretrial_loss_taxed",
        "_posttrial_loss_notax",
        "_posttrial_loss_taxed",
        "_total_loss_notax",
        "_total_loss_taxed",
    ]

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

    def build(self):
        


class CreditBuilder:
    """
    Builds the attributes for each credit earnings variable in the report.
    """

    def __init__(
        self, ea_main_dataclass: Any, pv_earnings_toggles: PVEarningsToggles
    ) -> None:
        self._raw = ea_main_dataclass
        self._pv_earnings_toggles = pv_earnings_toggles

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


class PVEarningsContextBuilder:
    """
    Builds the Jinja2 render context for PV_Earnings_Report_Template.

    All toggle flags and derived values that drive the template's conditional
    logic live here (not in the template, for simplicity's sake).

    Usage::

        ctx = PVEarningsContextBuilder(ea_main_dataclass, gui_toggles).build()

    When ``gui_toggles`` is provided the toggle values come directly from the
    GUI (checkboxes / comboboxes).  When omitted the builder falls back to
    inferring toggles from the extracted dataclass — used by the test harness
    and any headless / scripted invocation.
    """

    def __init__(
        self,
        ea_main_dataclass: Any,
        gui_toggles: PVEarningsToggles | None = None,
        base_builder: BaseBuilder | None = None,
        credit_builder: CreditBuilder | None = None,
    ) -> None:
        self._raw = ea_main_dataclass
        self._gui = gui_toggles
        self._base_builder = base_builder
        self._credit_builder = credit_builder

    # ── Public API ────────────────────────────────────────────────────────

    def build(self) -> dict[str, Any]:
        ctx: dict[str, Any] = {}
        ctx.update(self._all_fields())
        ctx.update(self._toggles())
        ctx.update(self._rehab_report_types())
        ctx.update(self._rehab_report_names(ctx["rehab_report_types"]))
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

    def _get_bases(self) -> set[str]:
        """
        Fallback method to determine the relevant bases (base1, base2, base3) for reference in report template.

        Returns:
            set[str]: The base earnings variables for the report.
        """

        # Regex to identify unique base instances
        bases = set()
        for key in self._raw.__dict__.keys():
            bases.update(re.findall(r"base(\d+)", key))

        for base in bases:
            base_var = f"base{base}"
            self._base_builder._bases.add(base_var)

        return bases

    def _get_credits(self) -> set[str]:
        """
        Fallback method to determine the relevant credits (credit1, credit2, credit3) for reference in report template.

        Returns:
            set[str]: The credit earnings variables for the report.
        """

        # Regex to identify unique credit instances
        credits = set()
        for key in self._raw.__dict__.keys():
            credits.update(re.findall(r"credit(\d+)", key))

        return credits

    def _get_meals_benefits(self) -> tuple[set[str], set[str]]:
        """
        Fallback method to check for the presence of meals and benefits variables for reference in report template.

        Returns:
            tuple[set[str], set[str]]: The meals and benefits variables for the report.
        """
        meals = set()
        for key in self._raw.__dict__.keys():
            meals.update(re.findall(r"meals", key))

        benefits = set()
        for key in self._raw.__dict__.keys():
            benefits.update(re.findall(r"benefits", key))

        return meals, benefits

    def _get_tax_rates(self) -> set[str]:
        """
        Determines the tax rates associated with relevant bases and credits.

        Returns:
            set[str]: The tax rate variables for the report.
        """
        tax_rates = set()
        for key in self._raw.__dict__.keys():
            tax_rates.update(re.findall(r"base\d+_tax_rate", key))
            tax_rates.update(re.findall(r"credit\d+_tax_rate", key))

        return tax_rates

    def _get_projection_type(self) -> set[str]:
        """
        Fallback method to determine projection type (WLE or To Age).
        """
        projection_types = set()
        for key in self._raw.__dict__.keys():
            projection_types.update(re.findall(r"WLE", key))
            projection_types.update(re.findall(r"toage", key))

        return projection_types

    def _toggles(self) -> dict[str, Any]:
        """
        Return all boolean/string flags that drive template conditionals.

        When a PVEarningsToggles instance was supplied at construction time
        (i.e. the GUI is in use) those values are used directly.  Otherwise
        toggles are inferred from the extracted dataclass.

        projection_type_toggle:
            'WLE'   — work-life equivalent (most common)
            'To Age' — to-age projection
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
        bases = self._get_bases()
        credits = self._get_credits()
        meals, benefits = self._get_meals_benefits()
        tax_rates = self._get_tax_rates()
        projection_type = self._get_projection_type()

        return {
            "base1_toggle": "base1" in bases,
            "base2_toggle": "base2" in bases,
            "base3_toggle": "base3" in bases,
            "projection_type_toggle": "WLE" if "WLE" in projection_type else "To Age",
            "credit1_toggle": "credit1" in credits,
            "credit2_toggle": "credit2" in credits,
            "credit3_toggle": "credit3" in credits,
            "meals_toggle": "meals" in meals,
            "benefits_toggle": "benefits" in benefits,
            "taxed_toggle": len(tax_rates) > 0,
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

        else:
            return {"rehab_report_types": []}

    def _rehab_report_names(self, rehab_report_types: list[str]) -> dict[str, Any]:
        """
        Returns a list of rehab report proper names (i.e. "Life Care Plan", "Medical Cost Projection").
        """
        names_map = {
            "LCP": "Life Care Plan",
            "MCP": "Medical Cost Projection",
            "Voc": "Vocational Opinion",
        }
        return {r: names_map[r] for r in rehab_report_types}

    def _aliases(self) -> dict[str, Any]:
        """
        Resolves known variable-name inconsistencies between the template and the extracted dataclass.
        Each entry here temporarily documents the mismatch so it can be cleaned up in the template when convenient.
        """
        return {
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
            "earnings_projection_type": "WLE"
            if toggles["projection_type_toggle"] == "WLE"
            else "To Age",
            # Creates docxtpl-compatible list of relevant bases
            "bases_list": (
                ["base1", "base2", "base3"]
                if toggles["base1_toggle"]
                and toggles["base2_toggle"]
                and toggles["base3_toggle"]
                else ["base1", "base2"]
                if toggles["base1_toggle"]
                and toggles["base2_toggle"]
                and not toggles["base3_toggle"]
                else ["base1", "base3"]
                if toggles["base1_toggle"]
                and not toggles["base2_toggle"]
                and toggles["base3_toggle"]
                else ["base2", "base3"]
                if not toggles["base1_toggle"]
                and toggles["base2_toggle"]
                and toggles["base3_toggle"]
                else ["base1"]
                if toggles["base1_toggle"]
                and not toggles["base2_toggle"]
                and not toggles["base3_toggle"]
                else ["base2"]
                if not toggles["base1_toggle"]
                and toggles["base2_toggle"]
                and not toggles["base3_toggle"]
                else ["base3"]
                if not toggles["base1_toggle"]
                and not toggles["base2_toggle"]
                and toggles["base3_toggle"]
                else []
            ),
            "credits_list": (
                ["credit1", "credit2", "credit3"]
                if toggles["credit1_toggle"]
                and toggles["credit2_toggle"]
                and toggles["credit3_toggle"]
                else ["credit1", "credit2"]
                if toggles["credit1_toggle"]
                and toggles["credit2_toggle"]
                and not toggles["credit3_toggle"]
                else ["credit1", "credit3"]
                if toggles["credit1_toggle"]
                and not toggles["credit2_toggle"]
                and toggles["credit3_toggle"]
                else ["credit2", "credit3"]
                if not toggles["credit1_toggle"]
                and toggles["credit2_toggle"]
                and toggles["credit3_toggle"]
                else ["credit1"]
                if toggles["credit1_toggle"]
                and not toggles["credit2_toggle"]
                and not toggles["credit3_toggle"]
                else ["credit2"]
                if not toggles["credit1_toggle"]
                and toggles["credit2_toggle"]
                and not toggles["credit3_toggle"]
                else ["credit3"]
                if not toggles["credit1_toggle"]
                and not toggles["credit2_toggle"]
                and toggles["credit3_toggle"]
                else []
            ),
            "growth_rate_projection": (
                "SSA"
                if (
                    (
                        toggles["projection_type_toggle"] == "WLE"
                        and int(self._get("claimant_WLE_from_trial_int")) >= 11
                    )
                    or (
                        toggles["projection_type_toggle"] == "To Age"
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
