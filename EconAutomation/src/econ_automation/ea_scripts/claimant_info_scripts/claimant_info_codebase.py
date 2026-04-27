from dataclasses import dataclass
from pathlib import Path
from itertools import batched
from datetime import date
import docx
import logging
import re

# Global logger module
logger = logging.getLogger(__name__)

class ClaimantInfoExtractor:
    def __init__(self, OFF_pathstr: str):
        # DEFINING CLASS VARIABLES
        self.OFF_pathstr = OFF_pathstr
        self.OFF_path = Path(OFF_pathstr)
        
        self.columns_dictionary = {}
        self.cleaned_columns_dictionary = {}
        self.usable_pairs = {}
        self.claimant_profile = {}
        
        # CALLING METHODS
        self.create_columns_dictionary()
        self.clean_columns_dictionary()
        self.create_usable_pairs()
        self.create_claimant_profile()

    def create_columns_dictionary(self) -> None:
        """
        Creates a dictionary to label each OFF table's column and its corresponding list of values from the open file form.
        """
        try:
            document = docx.Document(self.OFF_pathstr)
        except FileNotFoundError:
            logger.exception("ClaimantInfo.create_columns_dictionary: FileNotFoundError")
            raise
            
        table_list = []
        columns_dictionary = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [],}
        column_n = 0
        
        # Creates reference list of tables
        for table in document.tables:
            table_list.append(table)
        
        # Creates dictionary of columns (including empty value fields)
        for table in table_list:
            for column in table.columns:
                column_list = []
                column_n += 1
                for cells in column.cells:
                    column_list.append(cells.text)
                columns_dictionary[column_n] = column_list
                    
        self.columns_dictionary = columns_dictionary
                
    def clean_columns_dictionary(self) -> None:
        """
        Removes entirely empty formatting columns from the columns dictionary.
        """
        if self.columns_dictionary is None:
            return None
            
        cleaned_columns_dictionary = {}
        for column_key, value_list in self.columns_dictionary.items():
            for value in value_list:
                if value != '':
                    cleaned_columns_dictionary[column_key] = value_list
                    break
        self.cleaned_columns_dictionary = cleaned_columns_dictionary

    def create_usable_pairs(self) -> None:
        """
        Creates a dictionary of usable pairs from the cleaned columns dictionary and removes completely empty key:value pairs.
        """
        if self.cleaned_columns_dictionary is None:
            return None
            
        all_lists = []
        usable_pairs = {}
        address_counter = 0
        
        for value_list in self.cleaned_columns_dictionary.values():
            all_lists.append(value_list)
            
        for list_1, list_2 in batched(all_lists, 2):
            for item_1, item_2 in zip(list_1, list_2):
                if item_1 == '' and item_2 == '':
                    continue
                item_1 = item_1.strip(" ")
                item_2 = item_2.strip(" ")
                if item_1 == "Address:":
                    try:
                        if address_counter == 0:
                            address_counter += 1
                            item_1 = "firm_address"
                        else:
                            item_1 = "claimant_address"
                    except Exception:
                        raise Exception("Error creating address usable pairs")

                    usable_pairs[item_1] = item_2

                else:
                    try:
                        usable_pairs[item_1] = item_2
                    except Exception:
                        raise Exception("Error creating all usable pairs")

        self.usable_pairs = usable_pairs

    def create_claimant_profile(self) -> None:
        """
        Organizes claimant information from the usable pairs dictionary to make a "claimant profile," ready to be used universally.
        """
        if self.usable_pairs is None:
            raise Exception("ClaimantInfo.create_claimant_profile: self.usable_pairs not found")
            
        # PROACTIVELY CATCHING ERRORS
        if len(self.usable_pairs["Referral Source:"].split(" ")) > 2:
            self.usable_pairs["attorney_name_first"] = self.usable_pairs["Referral Source:"].split(" ")[0]
            self.usable_pairs["attorney_name_last"] = self.usable_pairs["Referral Source:"].split(" ")[-1]
            self.usable_pairs["attorney_name_middle"] = " ".join(self.usable_pairs["Referral Source:"].split(" ")[1:-1])
            self.usable_pairs["attorney_name_full"] = f"{self.usable_pairs['attorney_name_first']} {self.usable_pairs['attorney_name_middle']} {self.usable_pairs['attorney_name_last']}"
        else:
            self.usable_pairs["attorney_name_first"] = self.usable_pairs["Referral Source:"].split(" ")[0]
            self.usable_pairs["attorney_name_last"] = self.usable_pairs["Referral Source:"].split(" ")[-1]
            self.usable_pairs["attorney_name_middle"] = ""
            self.usable_pairs["attorney_name_full"] = f"{self.usable_pairs['attorney_name_first']} {self.usable_pairs['attorney_name_last']}"
            
        if len(self.usable_pairs["firm_address"].split("\n")) >= 2: # firm address
            self.usable_pairs["firm_address_1"] = self.usable_pairs["firm_address"].split("\n")[0]
            self.usable_pairs["firm_address_2"] = self.usable_pairs["firm_address"].split("\n")[1]
            self.usable_pairs["firm_address_full"] = f'{self.usable_pairs["firm_address_1"]} \n{self.usable_pairs["firm_address_2"]}'
        else:
            self.usable_pairs["firm_address_full"] = self.usable_pairs["firm_address"]
            self.usable_pairs["firm_address_1"] = self.usable_pairs["firm_address"]
            self.usable_pairs["firm_address_2"] = ""
            
        if len(self.usable_pairs["claimant_address"].split("\n")) >= 2: # claimant address
            self.usable_pairs["claimant_address_1"] = self.usable_pairs["claimant_address"].split("\n")[0]
            self.usable_pairs["claimant_address_2"] = self.usable_pairs["claimant_address"].split("\n")[1]
            self.usable_pairs["claimant_address_full"] = f'{self.usable_pairs["claimant_address_1"]} \n{self.usable_pairs["claimant_address_2"]}'
        else:
            self.usable_pairs["claimant_address_full"] = self.usable_pairs["claimant_address"]
            self.usable_pairs["claimant_address_1"] = self.usable_pairs["claimant_address"]
            self.usable_pairs["claimant_address_2"] = ""
            
        if len(self.usable_pairs["Name:"].split(" ")) > 2:
            self.usable_pairs["claimant_name_first"] = self.usable_pairs["Name:"].split(" ")[0]
            self.usable_pairs["claimant_name_last"] = self.usable_pairs["Name:"].split(" ")[-1]
            self.usable_pairs["claimant_name_middle"] = " ".join(self.usable_pairs["Name:"].split(" ")[1:-1])
            self.usable_pairs["claimant_name_full"] = f"{self.usable_pairs['claimant_name_first']} {self.usable_pairs['claimant_name_middle']} {self.usable_pairs['claimant_name_last']}"
        else:
            self.usable_pairs["claimant_name_first"] = self.usable_pairs["Name:"].split(" ")[0]
            self.usable_pairs["claimant_name_last"] = self.usable_pairs["Name:"].split(" ")[-1]
            self.usable_pairs["claimant_name_middle"] = ""
            self.usable_pairs["claimant_name_full"] = f"{self.usable_pairs['claimant_name_first']} {self.usable_pairs['claimant_name_last']}"
            
        # Corrects for erroneous Loggit merge that results in PascalCase addresses instead of newline-divided addresses
        text = self.usable_pairs["claimant_address_full"]
        pattern = r'^[A-Z][a-z]+(?:[A-Z][a-z]+)*$' # Checks for PascalCase
        split_text = re.sub(pattern, "\n", text)
        if re.match(pattern, text):
            self.usable_pairs["claimant_address_full"] = split_text
            self.usable_pairs["claimant_address_1"] = split_text.split("\n")[0]
            self.usable_pairs["claimant_address_2"] = split_text.split("\n")[1]
            
        text = self.usable_pairs["firm_address_full"]
        pattern = r'^[A-Z][a-z]+(?:[A-Z][a-z]+)*$' # Checks for PascalCase
        split_text = re.sub(pattern, "\n", text)
        if re.match(pattern, text):
            self.usable_pairs["firm_address_full"] = split_text
            self.usable_pairs["firm_address_1"] = split_text.split("\n")[0]
            self.usable_pairs["firm_address_2"] = split_text.split("\n")[1]
        
        claimant_profile = {
            "claimant_name_first": self.usable_pairs["claimant_name_first"],
            "claimant_name_first_initial": self.usable_pairs["claimant_name_first"][0],
            "claimant_name_last": self.usable_pairs["claimant_name_last"],
            "claimant_name_middle": self.usable_pairs["claimant_name_middle"],
            "claimant_name_full": self.usable_pairs["claimant_name_full"],
            "case_#": self.usable_pairs["Case #:"],
            "case_type": self.usable_pairs["Customer Type:"],
            "case_manager_name_full": self.usable_pairs["Counselor:"],
            "case_manager_name_first": self.usable_pairs["Counselor:"].split(" ")[0],
            "case_manager_name_last": self.usable_pairs["Counselor:"].split(" ")[-1],
            "case_manager_name_first_initial": self.usable_pairs["Counselor:"].split(" ")[0][0],
            "case_manager_name_last_initial": self.usable_pairs["Counselor:"].split(" ")[-1][0],
            "report_deadline": self.usable_pairs["Report Deadline:"],
            "addendum_report_deadline": "",
            "expert_designation_date": "",
            "mediation_date": self.usable_pairs["Mediation Date:"],
            "trial_date": self.usable_pairs["Trial Date:"],
            "discovery_cutoff": self.usable_pairs["Discover Cutoff:"],
            "attorney_name_first": self.usable_pairs["attorney_name_first"],
            "attorney_name_first_initial": self.usable_pairs["attorney_name_first"][0],
            "attorney_name_last": self.usable_pairs["attorney_name_last"],
            "attorney_name_middle": self.usable_pairs["attorney_name_middle"],
            "attorney_name_full": self.usable_pairs["attorney_name_full"],
            "firm_name": self.usable_pairs["Company Name:"],
            "firm_address_1": self.usable_pairs["firm_address_1"],
            "firm_address_2": self.usable_pairs["firm_address_2"],
            "firm_address_full": self.usable_pairs["firm_address_full"],
            "attorney_phone_#": self.usable_pairs["Telephone #:"],
            "attorney_fax_#": self.usable_pairs["Fax #:"],
            "attorney_email": self.usable_pairs["Email #1:"],
            "paralegal_name": self.usable_pairs["Paralegal:"],
            "paralegal_phone_#": "",
            "paralegal_email": self.usable_pairs["Email #2:"],
            "claimant_address_full": self.usable_pairs["claimant_address_full"],
            "claimant_address_2": self.usable_pairs["claimant_address_2"],
            "claimant_geozip": self.usable_pairs["claimant_address_2"].split(" ")[-1] if self.usable_pairs["claimant_address_2"].strip() else "",
            "claimant_phone_#": self.usable_pairs["Phone:"],
            "claimant_DOB": self.usable_pairs["Date of Birth:"],
            "claimant_age": self.usable_pairs["Age:"],
            "claimant_sex": self.usable_pairs["Gender:"],
            "claimant_DOI": self.usable_pairs["Injury Date:"],
            "claimant_DOI_2": self.usable_pairs["Injury Date 2:"],
            "claimant_injury_type(s)": self.usable_pairs["Injury Type:"],
            "court_jurisdiction": self.usable_pairs["Court:"],
            "date_opened": self.usable_pairs["Date Opened:"],
            "billing_rate": self.usable_pairs["Billing Rate:"],
        }
        
        # Removes duplicate injury date entries
        if claimant_profile["claimant_DOI_2"] == claimant_profile["claimant_DOI"]:
            claimant_profile["claimant_DOI_2"] = ""
        
        # Cleans up formatting for email addresses
        if claimant_profile["attorney_email"] != "":
            claimant_profile["attorney_email"] = claimant_profile["attorney_email"].lower()
        if claimant_profile["paralegal_email"] != "":
            claimant_profile["paralegal_email"] = claimant_profile["paralegal_email"].lower()
        
        # Adjust case_type naming convention
        if ("Life Care Plan" in claimant_profile["case_type"] 
            and "Vocational Analysis" in claimant_profile["case_type"] 
            and "Plaintiff" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Plaintiff", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Life Care Plan", "LCP-P")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Vocational Analysis", "Voc-P")
            claimant_profile["case_type"] = modified_case_type
        if ("Life Care Plan" in claimant_profile["case_type"] 
            and "Vocational Analysis" in claimant_profile["case_type"] 
            and "Defense" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Defense", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Life Care Plan", "LCP-D")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Vocational Analysis", "Voc-D")
            claimant_profile["case_type"] = modified_case_type
        if ("Life Care Plan" in claimant_profile["case_type"] and 
            "Plaintiff" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Plaintiff", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Life Care Plan", "LCP-P")
            claimant_profile["case_type"] = modified_case_type
        if ("Life Care Plan" in claimant_profile["case_type"] and 
            "Defense" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Defense", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Life Care Plan", "LCP-D")
            claimant_profile["case_type"] = modified_case_type
        if ("Vocational Analysis" in claimant_profile["case_type"] 
            and "Plaintiff" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Plaintiff", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Vocational Analysis", "Voc-P")
            claimant_profile["case_type"] = modified_case_type
        if ("Vocational Analysis" in claimant_profile["case_type"] 
            and "Defense" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Defense", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Vocational Analysis", "Voc-D")
            claimant_profile["case_type"] = modified_case_type
        if ("Medical Cost Projection" in claimant_profile["case_type"] 
            and "Plaintiff" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Plaintiff", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Medical Cost Projection", "MCP-P")
            claimant_profile["case_type"] = modified_case_type
        if ("Medical Cost Projection" in claimant_profile["case_type"] 
            and "Defense" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Defense", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Medical Cost Projection", "MCP-D")
            claimant_profile["case_type"] = modified_case_type
        if ("Medical Cost Projection" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace("Medical Cost Projection", "MCP")
            claimant_profile["case_type"] = modified_case_type
        if ("Medical Bill Audit" in claimant_profile["case_type"] 
            and "Plaintiff" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Plaintiff", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Medical Bill Audit", "MBA-P")
            claimant_profile["case_type"] = modified_case_type
        if ("Medical Bill Audit" in claimant_profile["case_type"] 
            and "Defense" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Defense", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Medical Bill Audit", "MBA-D")
            claimant_profile["case_type"] = modified_case_type
        if ("Medical Cost Analysis" in claimant_profile["case_type"] 
            and "Plaintiff" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Plaintiff", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Medical Cost Analysis", "MCA-P")
            claimant_profile["case_type"] = modified_case_type
        if ("Medical Cost Analysis" in claimant_profile["case_type"] 
            and "Defense" in claimant_profile["case_type"]):
            modified_case_type = claimant_profile["case_type"].replace(" - Defense", "")
            claimant_profile["case_type"] = modified_case_type
            modified_case_type = claimant_profile["case_type"].replace("Medical Cost Analysis", "MCA-D")
            claimant_profile["case_type"] = modified_case_type
        if "Review and Consult" in claimant_profile["case_type"]:
            modified_case_type = claimant_profile["case_type"].replace("Review and Consult", "R&C")
            claimant_profile["case_type"] = modified_case_type
        if "and" in claimant_profile["case_type"]:
            modified_case_type = claimant_profile["case_type"].replace("and", "&")
            claimant_profile["case_type"] = modified_case_type
        
        # Provides full version of claimant_sex
        if claimant_profile["claimant_sex"] == "M":
            claimant_profile["claimant_sex"] = "Male"
        elif claimant_profile["claimant_sex"] == "F":
            claimant_profile["claimant_sex"] = "Female"
        
        # Adds "claimant_gender" variable, e.g. "man" or "woman"; very much assumptive bigotry rn
        if claimant_profile["claimant_sex"] == "Male":
            claimant_profile["claimant_gender"] = "man"
        elif claimant_profile["claimant_sex"] == "Female":
            claimant_profile["claimant_gender"] = "woman"
        
        # Adds a "claimant_salutation", "claimant_gender_subjective", "claimant_gender_possessive", and "claimant_gender_objective" for integration with templates
        if claimant_profile["claimant_sex"] == "Male":
            claimant_profile["claimant_salutation"] = "Mr."
            claimant_profile["claimant_gender_subjective"] = "he"
            claimant_profile["claimant_gender_possessive"] = "his"
            claimant_profile["claimant_gender_objective"] = "him"
        elif claimant_profile["claimant_sex"] == "Female":
            claimant_profile["claimant_salutation"] = "Ms."
            claimant_profile["claimant_gender_subjective"] = "she"
            claimant_profile["claimant_gender_possessive"] = "her"
            claimant_profile["claimant_gender_objective"] = "her"
            
        # Creates claimant name variants
        claimant_profile["claimant_salutation_with_name_full"] = f"{claimant_profile['claimant_salutation']} {claimant_profile['claimant_name_full']}"
        claimant_profile["claimant_salutation_with_name_last"] = f"{claimant_profile['claimant_salutation']} {claimant_profile['claimant_name_last']}"
        
        # Creates attorney name variants
        claimant_profile["attorney_salutation"] = "Mr./Ms."
        claimant_profile["attorney_salutation_with_name_full_with_title"] = f"{claimant_profile['attorney_salutation']} {claimant_profile['attorney_name_full']}, Esq." # Includes Esq. title
        claimant_profile["attorney_salutation_with_name_full"] = f"{claimant_profile['attorney_salutation']} {claimant_profile['attorney_name_full']}"
        claimant_profile["attorney_salutation_with_name_last"] = f"{claimant_profile['attorney_salutation']} {claimant_profile['attorney_name_last']}"
        claimant_profile["attorney_name_full_with_title"] = f"{claimant_profile['attorney_name_full']}, Esq."
        
        # Corrects phone number formatting if hyphens aren't included
        if "-" not in claimant_profile["attorney_phone_#"]:
            original_number = claimant_profile["attorney_phone_#"]
            corrected_number = original_number[:3] + "-" + original_number[3:6] + "-" + original_number[6:]
            claimant_profile["attorney_phone_#"] = corrected_number
            
        if "-" not in claimant_profile["claimant_phone_#"]:
            original_number = claimant_profile["claimant_phone_#"]
            corrected_number = original_number[:3] + "-" + original_number[3:6]  + "-" + original_number[6:]
            claimant_profile["claimant_phone_#"] = corrected_number
        
        # Setting class variable claimant_profile
        self.claimant_profile = claimant_profile

@dataclass
class PersonName:
    name_first: str
    name_first_initial: str
    name_last: str
    name_last_initial: str
    name_middle: str
    name_full: str

@dataclass
class PersonInfo:
    name_salutation: str
    name_salutation_with_name_full: str
    name_salutation_with_name_last: str
    name_full_with_title: str
    name_sex: str
    name_gender: str
    name_subjective: str
    name_possessive: str
    name_objective: str

@dataclass
class PersonContact:
    phone_number: str
    fax_number: str
    email: str
    email_2: str

@dataclass
class PersonAddresses:
    address_1: str
    address_2: str
    address_city: str
    address_state: str
    address_zip: str
    address_full: str

@dataclass
class CaseDates:
    report_deadline: date
    addendum_report_deadline: date
    expert_designation_date: date
    mediation_date: date
    trial_date: date
    discovery_cutoff: date
    date_opened: date
    
@dataclass
class CaseDetails:
    case_number: str
    case_type: str
    case_manager_name_full: str
    case_manager_name_first: str
    case_manager_name_last: str
    case_manager_name_first_initial: str
    case_manager_name_last_initial: str
    court_jurisdiction: str
    billing_rate: str

@dataclass
class ClaimantDates:
    claimant_DOB: date
    claimant_DOI: date
    claimant_DOI_2: date

@dataclass
class AttorneyProfile(PersonName,PersonInfo,PersonContact,PersonAddresses):
    firm_name: str
    paralegal_name: str
    paralegal_phone_number: str
    paralegal_email: str
    attorney_phone_number: str
    attorney_fax_number: str
    attorney_email: str

@dataclass
class ClaimantProfile:
    
    # Initializing class variables to empty strings for the dataclass 
    claimant_name_full = PersonName.name_full
    claimant_name_last = PersonName.name_last
    claimant_name_first = PersonName.name_first
    claimant_name_middle = PersonName.name_middle
    claimant_name_first_initial = PersonName.name_first_initial
    claimant_name_last_initial = PersonName.name_last_initial
    claimant_address_full = PersonAddresses.address_full
    claimant_address_1 = PersonAddresses.address_1
    claimant_address_2 = PersonAddresses.address_2
    claimant_address_city = PersonAddresses.address_city
    claimant_address_state = PersonAddresses.address_state
    claimant_address_zip = PersonAddresses.address_zip
    claimant_phone_number = PersonContact.phone_number
    claimant_fax_number = PersonContact.fax_number
    claimant_email = PersonContact.email
    claimant_email_2 = PersonContact.email_2
    claimant_DOB = ClaimantDates.claimant_DOB
    claimant_DOI = ClaimantDates.claimant_DOI
    claimant_DOI_2 = ClaimantDates.claimant_DOI_2
    claimant_sex = PersonInfo.name_sex
    claimant_gender = PersonInfo.name_gender
    claimant_gender_subjective = PersonInfo.name_subjective
    claimant_gender_possessive = PersonInfo.name_possessive
    claimant_gender_objective = PersonInfo.name_objective
    claimant_salutation = PersonInfo.name_salutation
    claimant_salutation_with_name_full = PersonInfo.name_salutation_with_name_full
    claimant_salutation_with_name_last = PersonInfo.name_salutation_with_name_last
    
    def __post_init__(self):
        if not self.claimant_name:
            self.claimant_name = self.person_name.name_full
            self.claimant_name_last = self.person_name.name_last
            self.claimant_name_first = self.person_name.name_first
            self.claimant_name_middle = self.person_name.name_middle
            self.claimant_name_full = self.person_name.name_full
        if not self.claimant_address_1:
            self.claimant_address_1 = self.person_address
        if not self.claimant_address_2:
            self.claimant_address_2 = self.person_address
        if not self.claimant_address_full:
            self.claimant_address_full = self.person_address
        if not self.claimant_phone_number:
            self.claimant_phone_number = self.person_contact
        if not self.claimant_email:
            self.claimant_email = self.person_contact
        if not self.claimant_DOB:
            self.claimant_DOB = self.person_dates
        if not self.claimant_DOI:
            self.claimant_DOI = self.person_dates
        if not self.claimant_DOI_2:
            self.claimant_DOI_2 = self.person_dates
        if not self.claimant_sex:
            self.claimant_sex = self.person_info
        if not self.claimant_gender:
            self.claimant_gender = self.person_info
        if not self.claimant_gender_subjective:
            self.claimant_gender_subjective = self.person_info
        if not self.claimant_gender_possessive:
            self.claimant_gender_possessive = self.person_info
        if not self.claimant_gender_objective:
            self.claimant_gender_objective = self.person_info
        if not self.claimant_salutation:
            self.claimant_salutation = self.person_info
        if not self.claimant_salutation_with_name_full:
            self.claimant_salutation_with_name_full = self.person_info
        if not self.claimant_salutation_with_name_last:
            self.claimant_salutation_with_name_last = self.person_info
        if not self.claimant_name_full_with_title:
            self.claimant_name_full_with_title = self.person_info
        if not self.claimant_name_last_initial:
            self.claimant_name_last_initial = self.person_name
        if not self.claimant_name_first_initial:
            self.claimant_name_first_initial = self.person_name
        if not self.claimant_name_middle_initial:
            self.claimant_name_middle_initial = self.person_name
        self.claimant_name = PersonName(
            name_first=self.claimant_name,
            name_last=self.claimant_name,
            name_middle=self.claimant_name,
            name_full=self.claimant_name,
        )
        self.claimant_info = PersonInfo(
            name_salutation=self.claimant_info,
            name_salutation_with_name_full=self.claimant_info,
            name_salutation_with_name_last=self.claimant_info,
            name_full_with_title=self.claimant_info,
            name_sex=self.claimant_info,
            name_gender=self.claimant_info,
            name_subjective=self.claimant_info,
            name_possessive=self.claimant_info,
            name_objective=self.claimant_info,
        )
        self.claimant_contact = PersonContact(
            phone_number=self.claimant_contact,
            fax_number=self.claimant_contact,
            email=self.claimant_contact,
            email_2=self.claimant_contact,
        )
        self.claimant_address = PersonAddresses(
            address_1=self.claimant_address,
            address_2=self.claimant_address,
            address_city=self.claimant_address,
            address_state=self.claimant_address,
            address_zip=self.claimant_address,
            address_full=self.claimant_address,
        )
        self.claimant_dates = ClaimantDates(
            claimant_DOB=self.claimant_dates,
            claimant_DOI=self.claimant_dates,
            claimant_DOI_2=self.claimant_dates,
        )
    claimant_address_full: PersonAddresses
    claimant_address_1: PersonAddresses
    claimant_address_2: PersonAddresses
    claimant_city: PersonAddresses
    claimant_state: PersonAddresses
    claimant_zip: PersonAddresses
    claimant_phone_number: PersonContact
    claimant_DOB: date
    claimant_age: str
    claimant_sex: str
    claimant_gender: str
    claimant_DOI: date
    claimant_DOI_2: date
    claimant_injury_type: str
    
@dataclass
class CaseProfile(CaseDates,CaseDetails,AttorneyInfo,ClaimantDates,ClaimantInfo):