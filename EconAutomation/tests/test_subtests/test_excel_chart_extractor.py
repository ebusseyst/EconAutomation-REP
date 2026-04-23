import enum
import logging
import platform
from pathlib import Path
import unittest
import xlwings as xw
import pandas as pd
import pydantic
import pypdf

from ea_scripts.data_extraction_scripts.working_calc_extraction_codebase import WORKING_CALC_PATH_STR

# Test Module Logger    
logger = logging.getLogger(__name__)

# TEMP: Hardcode output chart directory file path
OUTPUT_CHART_DIR = Path(r"/Users/ericmacbook/Documents/GitHub/EconAutomation-REP/EconAutomation/ea_outputs/extracted_charts")


class TestExcelChartExtractorCore(unittest.TestCase):
    @classmethod
    def setUpClass(cls): # IF THIS WORKS, NEED TO SUBCLASS DATAEXTRACTORCORE AND CONVERT TO INIT
        cls.active_workbook_path = Path(WORKING_CALC_PATH_STR)
        cls.active_workbook = xw.Book(cls.active_workbook_path)
        
    def test_extract_sheet_charts(self, sheet_name: str):
        """
        Extracts charts as PDFs from the specified sheet of the active workbook.

        Args:
            chart_name (str): The name of the chart to extract.
        """
        success = False
        try:
            sheet = self.active_workbook.sheets[sheet_name]
            if platform.system() == "Darwin":
                sheet.page_setup.print_area = "H1:R35"
                sheet.to_pdf(str(Path(f"{OUTPUT_CHART_DIR}/{sheet_name}.pdf")))
                logger.info(f"test_extract_sheet_charts: Extracted {sheet_name} sheet pdf: {sheet.name}")
                
                pdf_path = Path(f"{OUTPUT_CHART_DIR}/{sheet_name}.pdf")
                pdf = pypdf.PdfReader(pdf_path)
                chart_page = pdf.pages[0]
                for image_index, image_object in enumerate(chart_page.images):
                    # filename = f"{OUTPUT_CHART_DIR}/{sheet_name}_chart_{image_object.name}"
                    # image_object.image.save(filename)
                    logger.info(f"image_object: {image_object}")
            else:
                for i, chart in enumerate(sheet.charts):
                    chart.to_pdf(f"{OUTPUT_CHART_DIR}/chart_{i}.pdf")
                    logger.info(f"test_extract_sheet_charts: Extracted {sheet_name} chart pdf: {chart.name}")
            success = True
            self.active_workbook.close()
        except Exception as e:
            logger.exception(f"test_extract_sheet_charts: Error extracting {sheet_name} chart pdf - {e}")
            success = False
            self.active_workbook.close()
        
        self.assertTrue(success)
        