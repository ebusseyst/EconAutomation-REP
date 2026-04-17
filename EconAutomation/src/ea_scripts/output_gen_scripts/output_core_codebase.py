import logging
from pathlib import Path

import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Module's logger instance
logger = logging.getLogger(__name__)
        

class WordTemplateProcessor:
    """
    A class that handles the autofilling of Word document templates with extracted data.
    """
    def __init__(self, extracted_data_dict: dict[str, any]=None, template_filepath: Path=None, output_save_path: Path=None):
        # DEFINING CLASS ATTRIBUTES
        self.variable_map = {}
        
        # DETERMINING TEMPLATE FILE PATH
        if template_filepath is None:
            try:
                raise ValueError("WordTemplateProcessor.__init__: template_filepath is None")
            except ValueError as e:
                logger.exception(e)
                return None
        else:
            self.template_filepath = template_filepath
            
        # DETERMINING OUTPUT SAVE PATH
        if output_save_path is None:
            try:
                raise ValueError("WordTemplateProcessor.__init__: output_save_path is None")
            except ValueError as e:
                logger.exception(e)
                return None
        else:
            self.output_save_path = output_save_path
        
        # DETERMINING VARIABLE MAP
        if extracted_data_dict is None:
            try:
                raise ValueError("WordTemplateProcessor.__init__: extracted_data_dict is None")
            except ValueError as e:
                logger.exception(e)
                return None
        else:
            for k,v in extracted_data_dict.items():
                variable_token = f"[[{k}]]" # creating the variable token
                self.variable_map[variable_token] = str(v) # converting all values to strings
                if self.variable_map[variable_token] is None:
                    self.variable_map[variable_token] = "" # replacing None values with empty strings
        
        # DEBUG
        for k,v in self.variable_map.items():
            logger.info(f"WordTemplateProcessor.__init__.variable_map: {k}: {v}")
        
        # LOADING WORD DOCUMENT TEMPLATE
        self.document = docx.Document(self.template_filepath)
        
        # CALLING METHODS
        self.autofill_relevant_paragraphs()
    
    def add_page_break_before_paragraph(self, paragraph):
        """
        Adds a page break before the provided paragraph.
        """
        pPr = paragraph._p.get_or_add_pPr()  # gets/creates the paragraph properties XML element
        pageBreakBefore = OxmlElement('w:pageBreakBefore')
        pPr.append(pageBreakBefore)
    
    def consolidate_paragraph_runs(self, paragraph):
        """
        Consolidates all writeable run text in a paragraph into the first run of that paragraph. 
        Paragraph text is preserved and is now editable, but mixed formatting is lost.
        """
        current_group = []
        
        if not paragraph.runs:
            return
        
        def run_has_image(run):
            """
            Checks if a run contains an image.
            """
            return run._r.find(qn('w:drawing')) is not None
        
        def consolidate_group(group):
            """
            Consolidates all writeable run text in a group into the first run of that group.
            """
            if len(group) <= 1:
                return
            full_text = "".join(r.text for r in group)
            group[0].text = full_text
            for r in group[1:]:
                r.text = ""
    
        for run in paragraph.runs:
            if run_has_image(run):
                consolidate_group(current_group)  # flush group before the image
                current_group = []                # reset for runs after the image
            else:
                current_group.append(run)
    
        consolidate_group(current_group)          # flush final group
    
    def replace_tokens_in_paragraphs(self, paragraphs, target_character="[["):
        """
        Replaces all variable tokens in the document's paragraphs with values from self.variable_map: {"variable_token": "replacement"}.
        """
        for paragraph in paragraphs:
            if target_character not in paragraph.text:
                continue
            
            self.consolidate_paragraph_runs(paragraph)
        
            for run in paragraph.runs:
                if run._r.find(qn('w:drawing')) is not None:
                    continue
                for token, value in self.variable_map.items():
                    run.text = run.text.replace(token, value)
                    
    def replace_tokens_in_tables(self, tables):
        """
        Replaces all variable tokens in the document's tables with values from self.variable_map: {"variable_token": "replacement"}.
        """
        for table in tables:
            for row in table.rows:
                for cell in row.cells:
                    self.replace_tokens_in_paragraphs(cell.paragraphs)
        
    def autofill_relevant_paragraphs(self, target_character="[["):
        """
        Executes the final autofill process, replacing all variable tokens in the document with values from variable_map: {"variable_token": "replacement"}.
        """
        try:
            self.replace_tokens_in_paragraphs(self.document.paragraphs, target_character)
            self.replace_tokens_in_tables(self.document.tables)
            
            for section in self.document.sections: # Using section targets for per-header iteration
                self.replace_tokens_in_paragraphs(section.header.paragraphs)
                self.replace_tokens_in_tables(section.header.tables)
                self.replace_tokens_in_paragraphs(section.footer.paragraphs)
                self.replace_tokens_in_tables(section.footer.tables)
                
            self.document.save(self.output_save_path)
            
        except Exception as e:
            logger.exception(f"WordTemplateProcessor.autofill_relevant_paragraphs() error: {e}")
            
    # def create_relevant_tables(self, extracted_tables_dict: dict[str, pd.DataFrame]=None, target_character="||"):
    #     """
    #     Replaces tables in the document based on the provided tables dictionary.
    #     """
    #     try:
    #         for worksheet_name, tables_dict in extracted_tables_dict.items():
    #             for table_name, table in tables_dict.items():
    #                 self.document.add_table(rows=table.shape[0], cols=table.shape[1])
    #                 self.document.tables[-1].style = "Table Grid"
    #                 for i, row in enumerate(table.iterrows()):
    #                     for j, value in enumerate(row[1]):
    #                     self.document.tables[-1].cell(i, j).text = str(value)
    #         logger.info(f"WordTemplateProcessor.create_relevant_tables: Created tables from {self.template_filepath}")
    #         logger.info(f"WordTemplateProcessor.create_relevant_tables: Created tables dict: {tables_dict}")
    #         return tables_dict
    #     except Exception as e:
    #         logger.exception(f"WordTemplateProcessor.create_relevant_tables: Error creating tables: {e}")
    #         return None