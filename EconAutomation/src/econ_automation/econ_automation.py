import logging
import logging.config

import yaml

from econ_automation.ea_scripts.ea_main_codebase import EconWorkflowAutomation

# Top-level logger instance
with open("src/econ_automation/logging_resources/logging_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
    
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    econ_workflow_automation = EconWorkflowAutomation()