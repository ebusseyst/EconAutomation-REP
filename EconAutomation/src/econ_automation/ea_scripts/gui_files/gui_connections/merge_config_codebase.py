from dataclasses import dataclass
from typing import Any


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
    earnings_projection_config: str = ""
    reference_type_config: str = ""
    
    PVLCP_report_config: bool = False
    PVearnings_report_config: bool = False
    
    base1_config: bool = False
    base2_config: bool = False
    base3_config: bool = False
    
    credit1_config: bool = False
    credit2_config: bool = False
    credit3_config: bool = False
    
    meals_config: bool = False
    
    taxstatus_config: bool = False
    
class ReportMergeConfigurator:
    def __init__(self, ea_main_dataclass: Any) -> None:
        self.ea_main_dataclass = ea_main_dataclass
        self.merge_config = MergeConfig()
        
        self.set_merge_config()
    
    def set_merge_config(self) -> None:
        """
        Sets the merge configuration k:v pairs to ea_main_dataclass.
        """
        self.ea_main_dataclass.earnings_projection_config = self.merge_config.earnings_projection_config
        self.ea_main_dataclass.reference_type_config = self.merge_config.reference_type_config
        
        self.ea_main_dataclass.PVLCP_report_config = self.merge_config.PVLCP_report_config
        self.ea_main_dataclass.PVearnings_report_config = self.merge_config.PVearnings_report_config
        
        self.ea_main_dataclass.base1_config = self.merge_config.base1_config
        self.ea_main_dataclass.base2_config = self.merge_config.base2_config
        self.ea_main_dataclass.base3_config = self.merge_config.base3_config
        
        self.ea_main_dataclass.credit1_config = self.merge_config.credit1_config
        self.ea_main_dataclass.credit2_config = self.merge_config.credit2_config
        self.ea_main_dataclass.credit3_config = self.merge_config.credit3_config
        
        self.ea_main_dataclass.meals_config = self.merge_config.meals_config
        
        self.ea_main_dataclass.taxstatus_config = self.merge_config.taxstatus_config
        
# THIS IS WHERE I LEFT OFF