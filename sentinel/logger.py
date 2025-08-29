import logging
import logging.handlers
import sys
import os
from pathlib import Path

# Default log file locations
SYSTEM_LOG_FILE = Path("/var/log/sentinel.log")
USER_LOG_FILE = Path.home() / ".sentinel" / "sentinel.log"


def setup_logger(name: str = "sentinel", level=logging.INFO) -> logging.Logger:
    """
    Setup a logger for Sentinel.
    Logs to:
      - stdout (for CLI users)
      - /var/log/sentinel.log (if writable, else ~/.sentinel/sentinel.log)
      - syslog (/dev/log) if available (RHEL/journald)
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger

    # --- Console handler (stdout) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # --- File handler ---
    log_file = SYSTEM_LOG_FILE
    if not log_file.parent.exists() or not os.access(log_file.parent, os.W_OK):
        # Fallback to user log dir
        USER_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        log_file = USER_LOG_FILE

    try:
        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"Could not set up file logging: {e}")

    # --- Syslog handler (only if /dev/log exists) ---
    if os.path.exists("/dev/log"):
        try:
            syslog_handler = logging.handlers.SysLogHandler(address="/dev/log")
            syslog_handler.setLevel(level)
            syslog_formatter = logging.Formatter("sentinel[%(process)d]: %(message)s")
            syslog_handler.setFormatter(syslog_formatter)
            logger.addHandler(syslog_handler)
        except Exception as e:
            logger.warning(f"Syslog not available: {e}")
    else:
        logger.info("Syslog not available (no /dev/log), skipping syslog logging.")

    return logger


# Create a default logger instance
logger = setup_logger()