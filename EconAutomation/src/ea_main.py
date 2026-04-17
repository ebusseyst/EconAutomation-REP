import logging

from ea_scripts.data_extraction_scripts.mastertemplate_extraction_codebase import MasterTemplateExtractor

# Top-level logger instance
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    mastertemplate_extractor = MasterTemplateExtractor()
    print(mastertemplate_extractor.extracted_data)