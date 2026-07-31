from dataclasses import dataclass


@dataclass
class MergeConfig:
    """
    Pre-defines variables to ensure consistency in report merge functionality.

    Usage:
        config = MergeConfig()
        config.base1_config
        config.meals_config
        config.taxstatus_config
    """

    PVLCP_report_config: bool = False
    PVearnings_report_config: bool = False

    earnings_projection_config: str = ""
    reference_type_config: str = ""

    base1_config: bool = False
    base2_config: bool = False
    base3_config: bool = False

    credit1_config: bool = False
    credit2_config: bool = False
    credit3_config: bool = False

    meals_config: bool = False
    benefits_config: bool = False

    taxstatus_config: bool = False
