"""Provides centralized logging configuration for Python applications."""

import logging
from colorlog import ColoredFormatter

# Define colors for different log levels
log_colors = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

# Custom formatter with colored output for console logs
detailed_formatter = ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    log_colors=log_colors,
)

simple_formatter = ColoredFormatter('%(log_color)s%(message)s', log_colors=log_colors)

# File formatter without color, for detailed logging to a file
file_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S'
)


def setup_logger(logger_name, use_simple_formatter=False):
    """
    Set up a logger instance with the specified name using the configured ColoredFormatter and
    writes all logs to a file.

    Args:
        logger_name (str): The name of the logger instance.
        use_simple_formatter (bool): Whether to use the simple formatter for console output.

    Returns:
        logging.Logger: The configured logger instance.
    """
    # Stream handler for console with colored output
    stream_handler = logging.StreamHandler()
    if use_simple_formatter:
        stream_handler.setFormatter(simple_formatter)
    else:
        stream_handler.setFormatter(detailed_formatter)

    # File handler for logging detailed information to app.log
    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setFormatter(file_formatter)

    # Create and configure the logger
    logger = logging.getLogger(logger_name)
    logger.addHandler(stream_handler)  # Add console handler
    logger.addHandler(file_handler)    # Add file handler
    logger.setLevel(logging.INFO)      # Set the desired logging level here

    return logger
