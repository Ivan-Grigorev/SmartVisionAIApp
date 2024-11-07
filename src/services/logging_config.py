"""Provides centralized logging configuration for Python applications."""

import logging
import tkinter as tk

from colorlog import ColoredFormatter

# Define colors for different log levels
log_colors = {
    'DEBUG': 'white',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

# Custom formatter with colored output
detailed_formatter = ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    log_colors=log_colors,
)


def setup_logger(logger_name):
    """
    Set up a logger instance with the specified name using the configured ColoredFormatter and
    writes all logs to a file.

    Attributes:
        logger_name (str): The name of the logger instance.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger(logger_name)

    if logger_name != 'root':
        # Stream handler for console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(detailed_formatter)
        logger.addHandler(stream_handler)

    logger.setLevel(logging.INFO)

    return logger


class TextHandler(logging.Handler):
    """
    A custom logging handler that directs log messages to a Tkinter Text widget, allowing
    real-time log display in a GUI application.
    """

    def __init__(self, text_widget):
        """
        Initialize the TextHandler with a Tkinter Text widget.

        Attributes:
            text_widget (tk.Text): The Tkinter widget that displays log messages.
        """

        super().__init__()
        self.text_widget = text_widget  # Store reference to the Text widget

    def emit(self, record):
        """
        Formats and appends a log record to the associated Tkinter Text widget.

        Attributes:
            record (logging.LogRecord): A LogRecord instance containing the event data.
        """
        msg = self.format(record)
        log_level = record.levelname  # Retrieve log level for tag-based coloring

        def append():
            # Check if widget still exists to avoid TclError if closed
            if self.text_widget.winfo_exists():
                self.text_widget.configure(state='normal')  # Enable editing to insert text
                self.text_widget.insert(tk.END, msg + '\n', log_level)  # Insert with color tag
                self.text_widget.configure(state='disabled')  # Re-disable editing
                self.text_widget.yview(tk.END)  # Auto-scroll to latest entry

        # Schedule append() on the main thread to ensure thread safety
        self.text_widget.after(2500, append)
