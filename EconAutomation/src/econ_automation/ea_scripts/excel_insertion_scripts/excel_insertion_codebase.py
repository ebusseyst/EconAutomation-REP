import logging
import sys
from pathlib import Path
from typing import Any

from econ_automation.ea_scripts.claimant_info_scripts.claimant_info_codebase import ClaimantInfo

# Logger instance
logger = logging.getLogger(__name__)

class ClaimantInfoInserter:
    def __init__(self, OFF_pathstr: str):
        # INSTANTIATING CLASS METHODS
        self.claimant_info = ClaimantInfo(OFF_pathstr)
        self.claimant_profile = self.claimant_info.claimant_profile
        
    def insert_mastertemplate_info(self):
        try:
            
        except Exception as e:
            logger.exception("ClaimantInfoInserter.insert_mastertemplate_info: Error inserting into MasterTemplate.")
            raise
        
        