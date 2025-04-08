"""Module to read IPTC, XMP, and EXIF metadata from images."""

import json
import re
import subprocess

from iptcinfo3 import IPTCInfo

from src.services.logging_config import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def get_metadata(image_path):
    """
    Get image metadata description from IPTC or XMP.

    Attributes:
        image_path (str): Path to the image file.

    Returns:
        str or None: Image description string, if available.
    """
    iptc_description = read_iptc_data(image_path)
    xmp_description = read_xmp_data(image_path)

    return iptc_description or xmp_description


def read_iptc_data(image_path):
    """
    Read IPTC metadata from the image.

    Attributes:
        image_path (str): Path to the image file.

    Returns:
        str or None: IPTC caption/abstract if found.
    """
    try:
        info = IPTCInfo(image_path)
        return info['caption/abstract']
    except Exception as e:
        logger.error(f"No IPTC metadata found. Error: {e}")
        return None


def read_xmp_data(image_path):
    """
    Read XMP metadata from the image using ExifTool.

    Attributes:
        image_path (str): Path to the image file.

    Returns:
        str or None: XMP description if available.
    """
    try:
        result = subprocess.run(
            ['exiftool', '-b', '-XMP', image_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        xmp_data = result.stdout.strip()

        match = re.search(
            r"<rdf:li\s+xml:lang=['\"]x-default['\"]>(.*?)</rdf:li>",
            xmp_data,
            re.DOTALL,
        )

        if match:
            return match.group(1).strip()
        return None

    except Exception as e:
        logger.error(f"No XMP metadata found. Error: {e}")
        return None


def read_exif_data(image_path):
    """
    Read EXIF metadata from the image using ExifTool.

    Attributes:
        image_path (str): Path to the image file.

    Returns:
        dict or None: EXIF metadata if found, otherwise None.
    """
    try:
        result = subprocess.run(
            ['exiftool', '-EXIF', '-json', image_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return json.loads(result.stdout)[0]
    except Exception as e:
        logger.error(f"No EXIF metadata found. Error: {e}")
        return None
