import logging
import logging.config
import datetime

import yaml

# Top-level test logger instance
logger = logging.getLogger(__name__)

# Setting up same logging config as main
with open("src/logging_resources/logging_config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

if __name__ == "__main__":
    # TEMP: PULLING TODAY'S DATE
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
