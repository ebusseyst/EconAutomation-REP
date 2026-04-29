from dataclasses import dataclass, field
from pathlib import Path
from itertools import batched
import datetime as dt
from dateutil.relativedelta import relativedelta
import logging
import re

import docx
from docx.document import Document as DocumentObject

logger = logging.getLogger(__name__)


# ── Helper: case type normalization ───────────────────────────────────────────

_CASE_TYPE_CODES = {
    "Life Care Plan": "LCP",
    "Vocational Analysis": "Voc",
    "Medical Cost Projection": "MCP",
    "Medical Bill Audit": "MBA",
    "Medical Cost Analysis": "MCA",
}


def _normalize_case_type(raw: str) -> str:
    """Converts verbose case type strings into short codes, e.g. 'Life Care Plan - Plaintiff' → 'LCP-P'."""
    ct = raw

    if " - Plaintiff" in ct:
        ct = ct.replace(" - Plaintiff", "")
        for long, short in _CASE_TYPE_CODES.items():
            ct = ct.replace(long, f"{short}-P")
    elif " - Defense" in ct:
        ct = ct.replace(" - Defense", "")
        for long, short in _CASE_TYPE_CODES.items():
            ct = ct.replace(long, f"{short}-D")
    else:
        for long, short in _CASE_TYPE_CODES.items():
            ct = ct.replace(long, short)

    ct = ct.replace("Review and Consult", "R&C")
    ct = ct.replace(" and ", " & ")
    return ct


# ── CaseProfile dataclass ─────────────────────────────────────────────────────


@dataclass
class CaseProfile:
    """
    A flat dataclass holding all case and claimant information.

    Sections
    --------
    INPUT fields    — set when you construct the object (everything with a plain default).
    DERIVED fields  — computed automatically by __post_init__; do not pass these to the constructor.

    Usage
    -----
        profile = CaseProfile(
            claimant_name_first="Jane",
            claimant_name_last="Doe",
            claimant_sex="Female",
            ...
        )
        # profile.claimant_name_full  →  "Jane Doe"
        # profile.claimant_salutation →  "Ms."
    """

    # ── INPUT: Claimant ───────────────────────────────────────────────
    claimant_name_first: str = ""
    claimant_name_middle: str = ""
    claimant_name_last: str = ""
    claimant_sex: str = ""  # expects "Male" or "Female"
    claimant_address_1: str = ""
    claimant_address_2: str = ""
    claimant_phone: str = ""
    claimant_DOB: str = ""
    claimant_age: str = ""
    claimant_DOI: str = ""
    claimant_DOI_2: str = ""
    claimant_injury_types: str = ""

    # ── INPUT: Case ───────────────────────────────────────────────────
    case_number: str = ""
    case_type: str = ""  # normalized automatically in __post_init__
    case_manager_name_full: str = ""
    court_jurisdiction: str = ""
    billing_rate: str = ""
    report_deadline_short: str = ""
    report_deadline_long: str = ""
    addendum_report_deadline_short: str = ""
    addendum_report_deadline_long: str = ""
    expert_designation_date_short: str = ""
    expert_designation_date_long: str = ""
    mediation_date_short: str = ""
    mediation_date_long: str = ""
    trial_date_short: str = ""
    trial_date_long: str = ""
    reference_date_short: str = ""
    reference_date_long: str = ""
    discovery_cutoff_short: str = ""
    discovery_cutoff_long: str = ""
    date_opened_short: str = ""
    date_opened_long: str = ""

    # ── INPUT: Attorney ───────────────────────────────────────────────
    attorney_name_first: str = ""
    attorney_name_middle: str = ""
    attorney_name_last: str = ""
    attorney_phone: str = ""
    attorney_fax: str = ""
    attorney_email: str = ""
    firm_name: str = ""
    firm_address_1: str = ""
    firm_address_2: str = ""

    # ── DERIVED: Claimant name ────────────────────────────────────────
    claimant_name_full: str = field(init=False, default="")
    claimant_name_first_initial: str = field(init=False, default="")
    claimant_name_last_initial: str = field(init=False, default="")

    # ── DERIVED: Claimant gender / salutation ─────────────────────────
    claimant_salutation: str = field(init=False, default="")
    claimant_salutation_with_name_full: str = field(init=False, default="")
    claimant_salutation_with_name_last: str = field(init=False, default="")
    claimant_gender: str = field(init=False, default="")
    claimant_gender_subjective: str = field(init=False, default="")
    claimant_gender_possessive: str = field(init=False, default="")
    claimant_gender_objective: str = field(init=False, default="")

    # ── DERIVED: Claimant address ─────────────────────────────────────
    claimant_address_full: str = field(init=False, default="")
    claimant_geozip: str = field(init=False, default="")

    # ── DERIVED: Case manager ─────────────────────────────────────────
    case_manager_name_first: str = field(init=False, default="")
    case_manager_name_last: str = field(init=False, default="")
    case_manager_name_first_initial: str = field(init=False, default="")
    case_manager_name_last_initial: str = field(init=False, default="")

    # ── DERIVED: Attorney name / salutation ───────────────────────────
    attorney_name_full: str = field(init=False, default="")
    attorney_name_first_initial: str = field(init=False, default="")
    attorney_name_last_initial: str = field(init=False, default="")
    attorney_name_full_with_title: str = field(init=False, default="")
    attorney_salutation: str = field(init=False, default="")
    attorney_salutation_with_name_full: str = field(init=False, default="")
    attorney_salutation_with_name_last: str = field(init=False, default="")
    attorney_salutation_with_name_full_with_title: str = field(init=False, default="")

    # ── DERIVED: Firm address ─────────────────────────────────────────
    firm_address_full: str = field(init=False, default="")

    def __post_init__(self):
        """Compute all derived fields from the input fields above."""

        # Claimant name
        name_parts = [
            self.claimant_name_first,
            self.claimant_name_middle,
            self.claimant_name_last,
        ]
        self.claimant_name_full = " ".join(p for p in name_parts if p)
        self.claimant_name_first_initial = (
            self.claimant_name_first[0] if self.claimant_name_first else ""
        )
        self.claimant_name_last_initial = (
            self.claimant_name_last[0] if self.claimant_name_last else ""
        )

        # Claimant gender / salutation
        # Each entry: (salutation, gender noun, subjective, possessive, objective)
        _gender_map = {
            "Male": ("Mr.", "man", "he", "his", "him"),
            "Female": ("Ms.", "woman", "she", "her", "her"),
        }
        sal, gen, subj, poss, obj = _gender_map.get(
            self.claimant_sex, ("", "", "", "", "")
        )
        self.claimant_salutation = sal
        self.claimant_gender = gen
        self.claimant_gender_subjective = subj
        self.claimant_gender_possessive = poss
        self.claimant_gender_objective = obj
        self.claimant_salutation_with_name_full = (
            f"{sal} {self.claimant_name_full}".strip()
        )
        self.claimant_salutation_with_name_last = (
            f"{sal} {self.claimant_name_last}".strip()
        )

        # Claimant address
        addr_parts = [self.claimant_address_1, self.claimant_address_2]
        self.claimant_address_full = "\n".join(p for p in addr_parts if p)
        self.claimant_geozip = (
            self.claimant_address_2.split(" ")[-1]
            if self.claimant_address_2.strip()
            else ""
        )

        # Claimant phone formatting
        if self.claimant_phone and "-" not in self.claimant_phone:
            n = self.claimant_phone
            self.claimant_phone = f"{n[:3]}-{n[3:6]}-{n[6:]}"

        # Claimant DOI deduplication
        if self.claimant_DOI_2 == self.claimant_DOI:
            self.claimant_DOI_2 = ""

        # Case type normalization
        self.case_type = _normalize_case_type(self.case_type)

        # Case manager name breakdown
        mgr_parts = self.case_manager_name_full.split()
        self.case_manager_name_first = mgr_parts[0] if mgr_parts else ""
        self.case_manager_name_last = mgr_parts[-1] if len(mgr_parts) > 1 else ""
        self.case_manager_name_first_initial = (
            self.case_manager_name_first[0] if self.case_manager_name_first else ""
        )
        self.case_manager_name_last_initial = (
            self.case_manager_name_last[0] if self.case_manager_name_last else ""
        )

        # Attorney name
        atty_parts = [
            self.attorney_name_first,
            self.attorney_name_middle,
            self.attorney_name_last,
        ]
        self.attorney_name_full = " ".join(p for p in atty_parts if p)
        self.attorney_name_first_initial = (
            self.attorney_name_first[0] if self.attorney_name_first else ""
        )
        self.attorney_name_last_initial = (
            self.attorney_name_last[0] if self.attorney_name_last else ""
        )

        # Attorney salutation / title variants
        self.attorney_salutation = "Mr./Ms."
        self.attorney_name_full_with_title = f"{self.attorney_name_full}, Esq."
        self.attorney_salutation_with_name_full = f"Mr./Ms. {self.attorney_name_full}"
        self.attorney_salutation_with_name_last = f"Mr./Ms. {self.attorney_name_last}"
        self.attorney_salutation_with_name_full_with_title = (
            f"Mr./Ms. {self.attorney_name_full}, Esq."
        )

        # Attorney phone formatting
        if self.attorney_phone and "-" not in self.attorney_phone:
            n = self.attorney_phone
            self.attorney_phone = f"{n[:3]}-{n[3:6]}-{n[6:]}"

        # Attorney email normalization
        self.attorney_email = self.attorney_email.lower()

        # Firm address
        firm_parts = [self.firm_address_1, self.firm_address_2]
        self.firm_address_full = "\n".join(p for p in firm_parts if p)


# ── OFFExtractor ────────────────────────────────────────────────────────────


class OFFExtractor:
    def __init__(self, OFF_filepath: Path):
        # INSTANTIATE CLASS ATTRIBUTES
        self.OFF_filepath = OFF_filepath
        self.OFF_pathstr = str(OFF_filepath)

        self.columns_dictionary = {}
        self.cleaned_columns_dictionary = {}
        self.usable_pairs = {}
        self.case_profile: CaseProfile | None = None

        document = self.load_OFF(OFF_pathstr=self.OFF_pathstr)
        self.create_columns_dictionary(document=document)
        self.cleaned_columns_dictionary = self.clean_columns_dictionary(
            columns_dictionary=self.columns_dictionary
        )
        self.usable_pairs = self.create_usable_pairs(
            columns_dictionary=self.cleaned_columns_dictionary
        )
        self.case_profile = self.create_case_profile(usable_pairs=self.usable_pairs)

    def load_OFF(self, OFF_pathstr: str) -> DocumentObject:
        """Load the claimant OFF document."""
        try:
            document = docx.Document(OFF_pathstr)
            return document
        except FileNotFoundError:
            logger.exception("ClaimantInfoExtractor.load_OFF: FileNotFoundError")
            raise

    def create_columns_dictionary(self, document: DocumentObject) -> None:
        """Labels each OFF table column with its list of cell values."""

        columns_dictionary = {n: [] for n in range(1, 11)}
        column_n = 0

        for table in document.tables:
            for column in table.columns:
                column_n += 1
                columns_dictionary[column_n] = [cell.text for cell in column.cells]

        self.columns_dictionary = columns_dictionary

    def clean_columns_dictionary(
        self, columns_dictionary: dict[int, list[str]]
    ) -> dict[int, list[str]]:
        """Removes entirely empty formatting columns."""
        return {
            k: v for k, v in columns_dictionary.items() if any(cell != "" for cell in v)
        }

    def create_usable_pairs(
        self, columns_dictionary: dict[int, list[str]]
    ) -> dict[str, str]:
        """Zips adjacent columns into label→value pairs, handling address disambiguation."""
        all_lists = list(columns_dictionary.values())
        usable_pairs = {}
        address_count = 0

        for list_1, list_2 in batched(all_lists, 2):
            for item_1, item_2 in zip(list_1, list_2):
                if item_1 == "" and item_2 == "":
                    continue
                item_1 = item_1.strip()
                item_2 = item_2.strip()

                if item_1 == "Address:":
                    item_1 = (
                        "firm_address" if address_count == 0 else "claimant_address"
                    )
                    address_count += 1

                usable_pairs[item_1] = item_2

        return usable_pairs

    # ── Private parsing helpers ───────────────────────────────────────

    @staticmethod
    def _parse_name(raw: str) -> tuple[str, str, str]:
        """Returns (first, middle, last) from a raw full-name string."""
        parts = raw.split()
        if len(parts) > 2:
            return parts[0], " ".join(parts[1:-1]), parts[-1]
        elif len(parts) == 2:
            return parts[0], "", parts[1]
        else:
            return raw, "", ""

    @staticmethod
    def _parse_address(raw: str) -> tuple[str, str]:
        """
        Returns (address_1, address_2) from a raw address string.
        Handles both newline-separated and PascalCase-merged addresses (Loggit merge artifact).
        """
        # Check for Loggit PascalCase merge artifact and split if needed
        pascal_pattern = r"^[A-Z][a-z]+(?:[A-Z][a-z]+)+$"
        if re.match(pascal_pattern, raw):
            raw = re.sub(r"(?<=[a-z])(?=[A-Z])", "\n", raw)

        lines = [ln.strip() for ln in raw.split("\n") if ln.strip()]
        if len(lines) >= 2:
            return lines[0], lines[1]
        return lines[0] if lines else "", ""

    @staticmethod
    def _format_date(raw: str) -> tuple[str, str]:
        """Parses a MM/DD/YYYY string and returns raw, 'Month DD, YYYY'."""
        try:
            return raw, dt.datetime.strptime(raw, "%m/%d/%Y").strftime("%B %d, %Y")
        except (ValueError, TypeError):
            return raw, raw

    @staticmethod
    def _determine_reference_date(
        report_deadline_short: str,
        trial_date_short: str | None = None,
    ) -> tuple[str, str]:
        """Determines the reference date based on the case type."""
        if trial_date_short:
            return OFFExtractor._format_date(trial_date_short)
        else:
            rep_datetime = dt.datetime.strptime(report_deadline_short, "%m/%d/%Y")
            ref_datetime = (rep_datetime + relativedelta(months=+3)).strftime(
                "%m/%d/%Y"
            )
            ref_datetime_short, ref_datetime_long = OFFExtractor._format_date(
                ref_datetime
            )

            return ref_datetime_short, ref_datetime_long

    @staticmethod
    def _expand_sex(raw: str) -> str:
        """Expands 'M'/'F' to 'Male'/'Female'."""
        return {"M": "Male", "F": "Female"}.get(raw, raw)

    # ── Main profile builder ──────────────────────────────────────────

    def create_case_profile(self, usable_pairs: dict[str, str]) -> CaseProfile | None:
        """
        Builds a CaseProfile dataclass from self.usable_pairs.
        All parsing and normalization that depends on the raw source data happens here.
        Derived fields (name variants, gender pronouns, etc.) are handled by CaseProfile.__post_init__.
        """
        up = usable_pairs  # shorthand

        # Parse names
        claimant_first, claimant_middle, claimant_last = self._parse_name(
            up.get("Name:", "")
        )
        attorney_first, attorney_middle, attorney_last = self._parse_name(
            up.get("Referral Source:", "")
        )

        # Parse addresses
        firm_addr_1, firm_addr_2 = self._parse_address(up.get("firm_address", ""))
        claimant_addr_1, claimant_addr_2 = self._parse_address(
            up.get("claimant_address", "")
        )

        # Date parsing
        report_deadline_short, report_deadline_long = self._format_date(
            up.get("Report Deadline:", "")
        )
        addendum_report_deadline_short, addendum_report_deadline_long = (
            self._format_date(up.get("Addendum Report Deadline:", ""))
        )
        expert_designation_date_short, expert_designation_date_long = self._format_date(
            up.get("Expert Designation Date:", "")
        )
        mediation_date_short, mediation_date_long = self._format_date(
            up.get("Mediation Date:", "")
        )
        trial_date_short, trial_date_long = self._format_date(up.get("Trial Date:", ""))
        discovery_cutoff_short, discovery_cutoff_long = self._format_date(
            up.get("Discover Cutoff:", "")
        )
        date_opened_short, date_opened_long = self._format_date(
            up.get("Date Opened:", "")
        )
        reference_date_short, reference_date_long = self._determine_reference_date(
            report_deadline_short, trial_date_short
        )

        self.case_profile = CaseProfile(
            # Claimant
            claimant_name_first=claimant_first,
            claimant_name_middle=claimant_middle,
            claimant_name_last=claimant_last,
            claimant_sex=self._expand_sex(up.get("Gender:", "")),
            claimant_address_1=claimant_addr_1,
            claimant_address_2=claimant_addr_2,
            claimant_phone=up.get("Phone:", ""),
            claimant_DOB=up.get("Date of Birth:", ""),
            claimant_age=up.get("Age:", ""),
            claimant_DOI=up.get("Injury Date:", ""),
            claimant_DOI_2=up.get("Injury Date 2:", ""),
            claimant_injury_types=up.get("Injury Type:", ""),
            # Case
            case_number=up.get("Case #:", ""),
            case_type=_normalize_case_type(up.get("Case Type:", "")),
            case_manager_name_full=up.get("Counselor:", ""),
            court_jurisdiction=up.get("Court:", ""),
            billing_rate=up.get("Billing Rate:", ""),
            report_deadline_short=report_deadline_short,
            report_deadline_long=report_deadline_long,
            addendum_report_deadline_short=addendum_report_deadline_short,
            addendum_report_deadline_long=addendum_report_deadline_long,
            expert_designation_date_short=expert_designation_date_short,
            expert_designation_date_long=expert_designation_date_long,
            mediation_date_short=mediation_date_short,
            mediation_date_long=mediation_date_long,
            trial_date_short=trial_date_short,
            trial_date_long=trial_date_long,
            reference_date_short=reference_date_short,
            reference_date_long=reference_date_long,
            discovery_cutoff_short=discovery_cutoff_short,
            discovery_cutoff_long=discovery_cutoff_long,
            date_opened_short=date_opened_short,
            date_opened_long=date_opened_long,
            # Attorney
            attorney_name_first=attorney_first,
            attorney_name_middle=attorney_middle,
            attorney_name_last=attorney_last,
            attorney_phone=up.get("Telephone #:", ""),
            attorney_fax=up.get("Fax #:", ""),
            attorney_email=up.get("Email #1:", ""),
            firm_name=up.get("Company Name:", ""),
            firm_address_1=firm_addr_1,
            firm_address_2=firm_addr_2,
        )
        return self.case_profile
