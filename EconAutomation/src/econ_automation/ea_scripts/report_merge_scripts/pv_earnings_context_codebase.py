import logging
import re
from dataclasses import dataclass, field, fields, is_dataclass
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


class BaseBuilder:
    """
    Builds the attributes for each base earnings variable in the report.
    """

    def __init__(
        self,
        ea_main_dataclass: Any,
        pv_earnings_toggles: PVEarningsToggles,
    ) -> None:
        """
        Initializes the BaseBuilder.

        Args:
            ea_main_dataclass: The EA main dataclass.
            pv_earnings_toggles: The GUI-provided PV Earnings toggles.
        """
        # Defining class attributes from arguments
        self._raw = ea_main_dataclass
        self._pv_earnings_toggles = pv_earnings_toggles

        # Determine which base numbers are present, based on GUI toggles
        self._base_numbers = set()
        if self._pv_earnings_toggles.base1_toggle:
            self._base_numbers.add(1)
        if self._pv_earnings_toggles.base2_toggle:
            self._base_numbers.add(2)
        if self._pv_earnings_toggles.base3_toggle:
            self._base_numbers.add(3)

        # If no base toggles are set to true, run fallback inference to determine which bases are present
        if not self._base_numbers:
            self._base_numbers = self._get_base_numbers()

        # Obtain list of projection types present based on GUI toggle
        self._projection_types = set()
        if self._pv_earnings_toggles.projection_type_toggle == "WLE":
            self._projection_types.add("WLE")
        if self._pv_earnings_toggles.projection_type_toggle == "toage":
            self._projection_types.add("toage")

        # Fallback: If no projection types are set, run inference
        if not self._projection_types:
            self._projection_types = self._get_projection_types()

        # Obtain nested dict with confirmed base varnames per unique base instance
        self.confirmed_base_vars = self._get_confirmed_base_vars()

        # Obtain list of BaseOrCredit instances, each containing confirmed variables for a unique base.
        self.base_instances = self.build_all_bases(
            ea_main_dataclass=self._raw,
            base_numbers=self._base_numbers,
            confirmed_base_vars=self.confirmed_base_vars,
        )

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

    def _get_base_numbers(self):
        """
        Programmatically parse unique base numbers present in ea_main_dataclass.
        """
        bases = set()
        pattern = r"base(\d+)"
        for key in self._raw.__dict__:
            bases.update(re.findall(pattern, key))
        return bases

    def _get_projection_types(self):
        """
        Programmatically parse unique projection types present in ea_main_dataclass.
        """
        projection_types = set()
        pattern2 = r"(WLE|toage)"
        for key in self._raw.__dict__:
            projection_types.update(re.findall(pattern2, key))
        return projection_types

    def _get_confirmed_base_vars(self) -> dict[str, dict[str, Any]]:
        """
        Programmatically cross-reference ea_main_dataclass for each possible base variable.
        Example output: {"base1": {"base1_toage_earnings", "base1_toage_eff_tax_rate", ...},
                        "base2": {"base2_WLE_earnings", "base2_WLE_eff_tax_rate", ...}, ...}
        """

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

        confirmed_base_vars = {}

        for number in self._base_numbers:
            base_stem = f"base{number}"
            confirmed_base_vars[base_stem] = {}
            for proj in self._projection_types:
                for suffix in suffixes:
                    variable = f"{base_stem}_{proj}{suffix}"
                    if self._is_populated(variable):
                        confirmed_base_vars[base_stem][variable] = self._get(variable)
        return confirmed_base_vars

    def build_all_bases(
        self,
        ea_main_dataclass: Any,
        base_numbers: set[int],
        confirmed_base_vars: dict[str, dict[str, Any]],
    ):
        """Instantiates the Base class for each base number and populates the instance with non-null variables."""
        base_instances = []
        for number in base_numbers:
            base_instance = BaseOrCredit(
                base_or_credit="base",
                base_or_credit_number=number,
                ea_main_dataclass=ea_main_dataclass,
                confirmed_vars=confirmed_base_vars,
            )
            base_instances.append(base_instance)
        return base_instances


class CreditBuilder:
    """
    Builds the attributes for each credit earnings variable in the report.
    """

    def __init__(
        self,
        ea_main_dataclass: Any,
        pv_earnings_toggles: PVEarningsToggles,
    ) -> None:
        """
        Initializes the CreditBuilder.

        Args:
            ea_main_dataclass: The EA main dataclass.
            pv_earnings_toggles: The GUI-provided PV Earnings toggles.
        """
        # Defining class attributes from arguments
        self._raw = ea_main_dataclass
        self._pv_earnings_toggles = pv_earnings_toggles

        # Determine which credit numbers are present, based on GUI toggles
        self._credit_numbers = set()
        if self._pv_earnings_toggles.credit1_toggle:
            self._credit_numbers.add(1)
        if self._pv_earnings_toggles.credit2_toggle:
            self._credit_numbers.add(2)
        if self._pv_earnings_toggles.credit3_toggle:
            self._credit_numbers.add(3)

        # If no credit toggles are set to true, run fallback inference to determine which credits are present
        if not self._credit_numbers:
            self._credit_numbers = self._get_credit_numbers()

        # Obtain list of projection types present based on GUI toggle
        self._projection_types = set()
        if self._pv_earnings_toggles.projection_type_toggle == "WLE":
            self._projection_types.add("WLE")
        if self._pv_earnings_toggles.projection_type_toggle == "toage":
            self._projection_types.add("toage")

        # Fallback: If no projection types are set, run inference
        if not self._projection_types:
            self._projection_types = self._get_projection_types()

        # Obtain nested dict with confirmed credit varnames per unique credit instance
        self.confirmed_credit_vars = self._get_confirmed_credit_vars()

        self.credit_instances = self.build_all_credits(
            ea_main_dataclass=self._raw,
            credit_numbers=self._credit_numbers,
            confirmed_credit_vars=self.confirmed_credit_vars,
        )

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

    def _get_credit_numbers(self):
        """
        Programmatically parses unique credit numbers present in ea_main_dataclass.
        """
        credits = set()
        pattern = r"credit(\d+)"
        for key in self._raw.__dict__:
            credits.update(re.findall(pattern, key))
        return credits

    def _get_projection_types(self):
        """
        Programmatically parses unique projection types present in ea_main_dataclass.
        """
        projection_types = set()
        pattern2 = r"(WLE|toage)"
        for key in self._raw.__dict__:
            projection_types.update(re.findall(pattern2, key))
        return projection_types

    def _get_confirmed_credit_vars(self) -> dict[str, dict[str, Any]]:
        """
        Programmatically cross-reference ea_main_dataclass for each possible credit variable.
        Example output: {"credit1": {"credit1_toage_earnings", "credit1_toage_eff_tax_rate", ...},
                        "credit2": {"credit2_WLE_earnings", "credit2_WLE_eff_tax_rate", ...}, ...}
        """

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

        confirmed_credit_vars = {}

        for number in self._credit_numbers:
            credit_stem = f"credit{number}"
            confirmed_credit_vars[credit_stem] = {}
            for proj in self._projection_types:
                for suffix in suffixes:
                    variable = f"{credit_stem}_{proj}{suffix}"
                    if self._is_populated(variable):
                        confirmed_credit_vars[credit_stem][variable] = self._get(
                            variable
                        )
        return confirmed_credit_vars

    def build_all_credits(
        self,
        ea_main_dataclass: Any,
        credit_numbers: set[int],
        confirmed_credit_vars: dict[str, dict[str, Any]],
    ):
        """Instantiates the Credit class for each credit number and populates the instance with non-null variables."""
        credit_instances = []
        for number in credit_numbers:
            credit_instance = BaseOrCredit(
                base_or_credit="credit",
                base_or_credit_number=number,
                ea_main_dataclass=ea_main_dataclass,
                confirmed_vars=confirmed_credit_vars,
            )
            credit_instances.append(credit_instance)
        return credit_instances


class BaseOrCredit:
    def __init__(
        self,
        base_or_credit: str,
        base_or_credit_number: int,
        ea_main_dataclass: Any,
        confirmed_vars: dict[str, dict[str, Any]],
    ) -> None:
        """
        Creates a "base" or "credit" instance and assigns all relevant, non-null variables in the confirmed_base_vars or confirmed_credit_vars as attributes.
        Used for for-loop formatting within the docxtpl template.
        """

        # Store args
        self._base_or_credit = base_or_credit
        self._base_or_credit_number = base_or_credit_number
        self._raw = ea_main_dataclass

        # Create a sub-dict of confirmed_vars for the current base/credit number
        self._base_or_credit_vars_dict = confirmed_vars[
            f"{base_or_credit}{base_or_credit_number}"
        ]

        # Determine projection type for this base/credit (WLE or toage)
        self._projection_type = (
            "WLE"
            if any("_WLE_" in key for key in self._base_or_credit_vars_dict)
            else "toage"
        )

        # Create attributes to populate
        self._earnings = None
        self._eff_tax_rate = None
        self._growth_rate = None
        self._pretrial_loss_notax = None
        self._pretrial_loss_taxed = None
        self._posttrial_loss_notax = None
        self._posttrial_loss_taxed = None
        self._total_loss_notax = None
        self._total_loss_taxed = None

        # Populate base/credit attributes from confirmed bases/credits dict
        self._populate_earnings_attributes(
            base_or_credit_number=self._base_or_credit_number,
            projection_type=self._projection_type,
            base_or_credit_vars=self._base_or_credit_vars_dict,
        )

    def _populate_earnings_attributes(
        self,
        base_or_credit_number: int,
        projection_type: str,
        base_or_credit_vars: dict[str, Any],
    ):
        """
        Populates the instance attributes from the confirmed bases/credits dictionary.
        """
        for key, value in base_or_credit_vars.items():
            if (
                key
                == f"{self._base_or_credit}{base_or_credit_number}_{projection_type}_earnings"
            ):
                self._earnings = value
            elif (
                key
                == f"{self._base_or_credit}{base_or_credit_number}_{projection_type}_eff_tax_rate"
            ):
                self._eff_tax_rate = value
            elif (
                key
                == f"{self._base_or_credit}{base_or_credit_number}_{projection_type}_growth_rate"
            ):
                self._growth_rate = value
            elif (
                key
                == f"{self._base_or_credit}{base_or_credit_number}_{projection_type}_pretrial_loss_notax"
            ):
                self._pretrial_loss_notax = value
            elif (
                key
                == f"{self._base_or_credit}{base_or_credit_number}_{projection_type}_pretrial_loss_taxed"
            ):
                self._pretrial_loss_taxed = value
            elif (
                key
                == f"{self._base_or_credit}{base_or_credit_number}_{projection_type}_posttrial_loss_notax"
            ):
                self._posttrial_loss_notax = value
            elif (
                key
                == f"{self._base_or_credit}{base_or_credit_number}_{projection_type}_posttrial_loss_taxed"
            ):
                self._posttrial_loss_taxed = value
            elif (
                key
                == f"{self._base_or_credit}{base_or_credit_number}_{projection_type}_total_loss_notax"
            ):
                self._total_loss_notax = value
            elif (
                key
                == f"{self._base_or_credit}{base_or_credit_number}_{projection_type}_total_loss_taxed"
            ):
                self._total_loss_taxed = value
            else:
                continue


class PVEarningsContextBuilder:
    """
    Builds the Jinja2 render context for PV_Earnings_Report_Template.

    All toggle flags and derived values that drive the template's conditional
    logic live here (not in the template, for simplicity's sake).

    Usage::

        ctx = build_pv_earnings_context(ea_main_dataclass, gui_toggles)

    ``gui_toggles`` always drives the template's conditional flags — the
    module-level ``build_pv_earnings_context()`` entry point defaults it to a
    conservative ``PVEarningsToggles()`` when the GUI didn't supply one.
    ``base_builder``/``credit_builder`` additionally infer which base/credit
    numbers and projection types are actually present in the extracted
    dataclass whenever their corresponding toggles aren't set.
    """

    def __init__(
        self,
        ea_main_dataclass: Any,
        gui_toggles: PVEarningsToggles,
        base_builder: BaseBuilder,
        credit_builder: CreditBuilder,
    ) -> None:
        # Defining class attributes from arguments
        self._raw = ea_main_dataclass
        self._gui = gui_toggles
        self._base_builder = base_builder
        self._credit_builder = credit_builder

    def build(self) -> dict[str, Any]:
        ctx: dict[str, Any] = {}
        ctx.update(self._all_fields())
        ctx.update(self._toggles())
        ctx.update(self._rehab_report_types())
        ctx.update(self._rehab_report_names(ctx["rehab_report_types"]))
        ctx.update(self._derived_fields())
        ctx.update(self._aliases())
        # Per-base/credit instances for {% for base in base_instances %} style
        # template loops referencing e.g. base._earnings, base._growth_rate.
        ctx["base_instances"] = self._base_builder.base_instances
        ctx["credit_instances"] = self._credit_builder.credit_instances
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
        Return all boolean/string flags that drive template conditionals,
        sourced directly from the GUI-provided PVEarningsToggles instance.

        projection_type_toggle:
            'WLE'   — work-life equivalent (most common)
            'To Age' — to-age projection
        """
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

    def _rehab_report_types(self) -> dict[str, Any]:
        """
        Builds the ``rehab_report_types`` list consumed by:
            {% if 'LCP' in rehab_report_types %}
            {% if 'MCP' in rehab_report_types %}
            {% if 'Voc' in rehab_report_types %}
        """
        return {"rehab_report_types": list(self._gui.rehab_report_types)}

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
    toggles = gui_toggles or PVEarningsToggles()
    base_builder = BaseBuilder(ea_main_dataclass, toggles)
    credit_builder = CreditBuilder(ea_main_dataclass, toggles)
    return PVEarningsContextBuilder(
        ea_main_dataclass, toggles, base_builder, credit_builder
    ).build()
