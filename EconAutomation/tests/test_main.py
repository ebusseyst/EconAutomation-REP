import logging
import logging.config
from pathlib import Path
import datetime
import sys

import yaml

from test_subtests.test_excel_chart_extractor import TestExcelChartExtractorCore

# TEMP: Add path to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Setting up same logging config as main
with open("/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/tests/logging_resources/logging_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
    
# Top-level test logger instance
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    test_work_calc_chart_extractor = TestExcelChartExtractorCore()
    test_work_calc_chart_extractor.setUpClass()
    test_work_calc_chart_extractor.test_extract_sheet_charts("GetBloombergDailyYieldCurve_cur")