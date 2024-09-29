"""
Logger initialization module for the Discord bot.

This module sets up a logger to handle logging for the bot. It creates a log directory if it 
does not already exist and configures a rotating file handler to manage log files with a 
maximum size of 5 MB and a backup count of 5. Additionally, it sets up a console handler 
to output logs to the console. The logger is configured to use the INFO log level by default.
"""

import os
import logging
from logging.handlers import RotatingFileHandler


def init_logger():
    """Initialize and configure the logger.

    Creates a log directory, sets up a rotating file handler with a size limit,
    and a console handler for outputting logs.
    """
    # Create the log directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Set up rotating file handler (5 MB limit with 5 backups)
    log_file_path = os.path.join(log_dir, "bot.log")
    rotating_file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=5 * 1024 * 1024,  # 5 MB per log file
        backupCount=5,  # Keep up to 5 backup files
        encoding="utf-8",
    )

    # Console handler (to print logs to console)
    console_handler = logging.StreamHandler()

    # Define log format
    log_format = logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")

    # Set formatter for both handlers
    rotating_file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)

    # Create logger and add handlers
    logger_instance = logging.getLogger("bot")
    logger_instance.setLevel(logging.INFO)  # Set default log level to INFO

    # Check if handlers are already added to avoid duplication
    if not logger_instance.handlers:
        logger_instance.addHandler(rotating_file_handler)
        logger_instance.addHandler(console_handler)

    return logger_instance


# Initialize the logger instance
logger = init_logger()
