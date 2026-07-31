import logging
import logging.config
import os
from datetime import datetime
from pathlib import Path
import traceback
import sys

import yaml
from pythonjsonlogger import jsonlogger

from econ_automation._version import APP_NAME, __version__ as APP_VERSION


def _get_log_dir() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or (Path.home() / "AppData" / "Roaming"))
        return base / APP_NAME / "logs"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Logs" / APP_NAME
    else:
        return Path.home() / ".local" / "share" / APP_NAME / "logs"


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


class TimestampedJSONFileHandler(logging.FileHandler):
    def __init__(self, max_logs: int = 10):
        log_dir = _get_log_dir()
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_path = log_dir / f"econ_automation_{timestamp}.txt"
        super().__init__(str(log_path), mode="a", delay=False)
        self.setFormatter(DefaultJSONFormatter())
        self.terminator = "\n\n"
        sys.excepthook = self._handle_exception
        self._purge_old_logs(log_dir, max_logs)

    @staticmethod
    def _purge_old_logs(log_dir: Path, max_logs: int) -> None:
        logs = sorted(
            log_dir.glob("econ_automation_*.txt"),
            key=lambda p: p.stat().st_mtime,
        )
        for old_log in logs[:-max_logs]:
            try:
                old_log.unlink()
            except Exception:
                pass

    def _handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.getLogger(__name__).critical(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )


def setup_logging():
    config_path = Path(__file__).parent / "logging_config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    logging.config.dictConfig(config)
