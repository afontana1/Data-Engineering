import logging
import logging.handlers
from pathlib import Path
import sys


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    green = "\x1b[32;1m"
    yellow = "\x1b[33;1m"
    red = "\x1b[31;1m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    end_color = "\x1b"
    format = "{color}%(levelname)s\x1b[0m: %(asctime)s  -  %(message)s"

    FORMATS = {
        logging.DEBUG: format.replace("{color}", grey),
        logging.INFO: format.replace("{color}", green),
        logging.WARNING: format.replace("{color}", yellow),
        logging.ERROR: format.replace("{color}", bold_red),
        logging.CRITICAL: format.replace("{color}", bold_red),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger() -> logging.Logger:
    """Configure logging for the MCP client with log rotation."""
    logger = logging.getLogger("client-mcp")

    # Remove existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Define a consistent log directory in the user's home folder
    log_dir = Path.home() / ".local" / "share" / "fastchat-mcp"
    log_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    # Define the log file path
    log_file = log_dir / "mcp_client.log"

    # Create a rotating file handler
    # - Rotate when log reaches 5MB
    # - Keep 3 backup files
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding="utf-8",
    )

    # Add formatter to file handler
    file_handler.setFormatter(CustomFormatter())

    # Add handler to logger
    logger.addHandler(file_handler)

    # Terminal Handler  (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    # Set level
    logger.setLevel(logging.DEBUG)

    return logger


class LoggerFeatures:
    LOGO: str = f"""{CustomFormatter.green}
             _ __ ___ ______           __        __          __    
            _ __ ___ / ____/___  _____/ /_ _____/ /    ___  / /_
           _ __ ___ / /_  / __ `/ ___/ __/ ____/ /_  / __ `/___/
          _ __ ___ / __/ / /_/ (__  ) /_/ (___/ __ \/ /_/ / /_ 
         _ __ ___ /_/    \__,_/____/\__/\____/_/ /_/\__,__\__/ 
    """


logger = setup_logger()
