"""Module to check and create a path to data files."""

import os
import platform
import sys


def app_storage(op_system, filename):
    """
    Create and return the full path to a file in the application specific storage directory.

    Attributes:
        op_system (str): The operating system name.
        filename (str): The name of the file to create or access in the app storage.

    Returns:
        str: The full path to the file in the app's storage directory.
    """
    if op_system == 'Darwin':  # macOS
        app_support_dir = os.path.expanduser('~/Library/Application Support/SmartVisionAI/')
    elif op_system == 'Windows':
        app_support_dir = os.path.expanduser('~/AppData/Local/SmartVisionAI/')
    else:
        # Other operating systems
        app_support_dir = os.path.expanduser('~/.SmartVisionAI')

    os.makedirs(app_support_dir, exist_ok=True)

    return os.path.join(app_support_dir, filename)


def get_data_file_path(filename):
    """
    Return the full path to a specified data file, handling PyInstaller bundles and local source runs.

    Attributes:
        filename (str): The name of the file to locate or create.

    Returns:
        str: The full file path to the data file.
    """

    # Check if running in PyInstaller bundle
    if hasattr(sys, '_MEIPASS'):
        # Get the operating system name
        op_system = platform.system()
        file_path = app_storage(op_system, filename)
    else:
        # When running directly from the source
        file_path = os.path.join('src', 'data', filename)

    return file_path
