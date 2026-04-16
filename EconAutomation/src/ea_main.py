import logging

from ea_scripts.ea_main_codebase import *

# Top-level logger instance
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    working_calc_extractor = WorkingCalcExtractor()
    print(working_calc_extractor.extracted_data)