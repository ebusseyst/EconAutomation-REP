import logging
import logging.config
import traceback

from pythonjsonlogger import jsonlogger

from ea_scripts.ea_main_codebase import APP_NAME, APP_VERSION

# Sets global attribute, which is then injected via handler filter
class GlobalContextFilter(logging.Filter):
    def __init__(self, name='', **fields):
        super().__init__(name)
        self._fields = {
            "app_name": APP_NAME,
            "version": APP_VERSION,
            **fields
        }
        
    def filter(self, record: logging.LogRecord):
        record.app_name = self.app_name
        record.version = self.version
        for key, value in self._fields.items(): # Iterates through the _fields dictionary and assigns each key-value pair as an attribute to the record
            setattr(record, key, value)
        return True # Always passes through

class DefaultJSONFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(json_indent=2, *args, **kwargs)
        
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        
        if record.exc_info:
            exc_type, exc_value, exc_traceback = record.exc_info
            log_record["exception"] = {
                "exception_type": exc_type.__name__,
                "exception_value": str(exc_value),
                "traceback": traceback.format_exception(exc_type, exc_value, exc_traceback)
            }
            
            log_record.pop('exc_info', None)
            log_record.pop('exc_text', None)      

class DefaultConsoleFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def formatException(self, ei) -> str:
        return "".join(traceback.format_exception(*ei)).rstrip()
        
# # Helper function to log case events (by bypassing wrappers and identifying the actual caller)
# def log_case_event(msg, *args, **kwargs):
#     logger.info(msg, *args, stacklevel=2, **kwargs)
#     # stacklevel=2 → attributes point to the caller of log_case_event