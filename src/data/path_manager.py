"""Module to check and create a path to data files."""

import os
import sys


def get_data_file_path(filename):
    """
    Return the full path to a specified data file, adjusting for PyInstaller bundles.

    Attributes:
        filename (str): The name of the file to locate within the `data` directory.

    Returns:
        str: The full file path to `filename` within the `data` directory.
    """
    if hasattr(sys, '_MEIPASS'):
        # When running in a PyInstaller bundle
        return os.path.join(sys._MEIPASS, 'data', filename)
    else:
        # When running directly from the source
        return os.path.join('src', 'data', filename)
