import logging
import logging.config
from logging.handlers import RotatingFileHandler
from pathlib import Path
import traceback
import sys
from importlib.metadata import version, metadata

from pythonjsonlogger import jsonlogger

# Load app name and version from package metadata
APP_NAME = metadata("econ_automation").get("Name")
APP_VERSION = version("econ_automation")


# Set global attribute, which is then injected via handler filter
class GlobalContextFilter(logging.Filter):
    def __init__(self, name="", **fields):
        super().__init__(name)
        self._fields = {"app_name": APP_NAME, "version": APP_VERSION, **fields}

    def filter(self, record: logging.LogRecord):
        for key, value in self._fields.items():
            setattr(record, key, value)
        return True


class DefaultJSONFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(json_indent=2, *args, **kwargs)

    def add_fields(self, log_data, record, message_dict):
        super().add_fields(log_data, record, message_dict)

        if record.exc_info:
            exc_type, exc_value, exc_traceback = record.exc_info
            log_data["exception"] = {
                "exception_type": exc_type.__name__,
                "exception_value": str(exc_value),
                "traceback": traceback.format_exception(
                    exc_type, exc_value, exc_traceback
                ),
            }

            log_data.pop("exc_info", None)
            log_data.pop("exc_text", None)


class DefaultConsoleFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def formatException(self, ei) -> str:
        return "".join(traceback.format_exception(*ei)).rstrip()
    
_DEFAULT_LOG_PATH = str(Path(__file__).parent.parent.parent / "logs" / "crash.json")


class JSONFileHandler(RotatingFileHandler):
    def __init__(self, filename=_DEFAULT_LOG_PATH, maxBytes=500000, backupCount=5, mode='a', delay=True):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        super().__init__(filename, maxBytes=maxBytes, backupCount=backupCount, mode=mode, delay=delay)
        self.setFormatter(DefaultJSONFormatter())
        sys.excepthook = self._handle_exception

    def _handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.getLogger(__name__).critical(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )
        