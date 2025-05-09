"""This module processes images by generating descriptive metadata using GPT and adds the metadata to images."""

import os
import shutil
import sys
import tempfile
import time

from iptcinfo3 import IPTCInfo

from src.services.check_access import terminate_processes_using_file
from src.services.files_filter import filter_files_by_extension
from src.services.img_metadata_reader import get_metadata
from src.services.logging_config import setup_logger
from src.services.process_timer import execution_timer
from src.services.response_parser import parse_response

# Initialize logger using the setup function
logger = setup_logger(__name__)


class ImagesDescriber:
    """
    A class to facilitate image description generation using OpenAI's GPT model and add metadata to images.

    Methods:
        add_metadata():
            Adds processed titles, descriptions, and keywords to the metadata of the images in the source directory.
            Saves the processed images in the destination directory.

        remove_backup_file(filename):
            Static method. Removes the backup file created by the IPTCInfo library, if it exists.
            Typically, backup files have a '~' suffix.

        __str__():
            Returns a string representation of the ImagesDescriber instance.
    """

    def __init__(self, prompt, src_path, dst_path, author_name):
        """
        Initialize the ImagesDescriber with a prompt, source path, destination path, and author name.

        Attributes:
            prompt (str): The prompt to be sent to the GPT model for generating descriptions.
            src_path (str): The path to the directory containing the images to be processed.
            dst_path (str): The path to the directory where processed images will be saved. Defaults to src_path if not provided.
            author_name (str): The name of the author for the images.
        """
        self.prompt = prompt
        self.src_path = src_path
        self.dst_path = dst_path if dst_path else src_path
        self.author_name = author_name

    def add_metadata(self):
        """
        Add processed titles and keywords to the metadata of images in the source directory.

        Saves the processed images in the destination directory.
        """
        # Record the start time of the process of handling the images
        time_start = time.perf_counter()

        # Initialize counter for images
        processed_count = 0

        # Get filtered image files to process
        filtered_image_files = filter_files_by_extension(src_path=self.src_path)

        # Check if image files exist, stop processing if not
        if not filtered_image_files:
            logger.warning(
                f"No image files found in the source folder {self.src_path} to process. Please verify and try again."
            )
            # Exit the program with a status code 1
            sys.exit(1)

        logger.info(
            f"Images processing has started! {len(filtered_image_files)} images to process."
        )

        # Get title, description, and keywords for each image file
        for image_name in filtered_image_files:
            image_path = os.path.join(self.src_path, image_name)
            destination_path = os.path.join(self.dst_path, image_name)

            # Ensure destination directory exists; create if it doesn't
            if not os.path.exists(destination_path):
                os.makedirs(self.dst_path, exist_ok=True)

            # Terminate processes using the image file
            terminate_processes_using_file(image_path)

            # Track if image processing succeeds
            successfully_processed = False

            try:
                with open(image_path, 'rb') as image_file:
                    # Create a temporary copy of the image
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        temp_image_path = temp_file.name
                    shutil.copyfile(image_path, temp_image_path)

                    # Load IPTC metadata or create a new one
                    try:
                        info = IPTCInfo(temp_image_path)
                    except Exception as e:
                        logger.error(f"No IPTC metadata found, create a new one. Error: {e}")
                        info = IPTCInfo(None)

                    # Get image caption from image metadata
                    image_caption = get_metadata(temp_image_path)
                    if not image_caption:
                        logger.warning(
                            f"The file '{image_name}' does not contain metadata. "
                            "Title, description, and keywords will be generated "
                            "without using the image caption."
                        )

                    # Get cleaned data from GPT response
                    title, description, keywords = parse_response(
                        image_file=image_file,
                        prompt=self.prompt,
                        image_caption=image_caption,
                    )

                    # Modify metadata on the temporary file
                    info['object name'] = title
                    info['caption/abstract'] = description
                    info['keywords'] = keywords
                    info['by-line'] = self.author_name

                    # Save the modified metadata back to the temp file
                    info.save_as(temp_image_path)
                    shutil.move(temp_image_path, destination_path)
                    logger.info(
                        f"Metadata added to {image_name} (JPEG) "
                        f"{'and moved to ' + os.path.dirname(destination_path) if destination_path != image_path else ''}"
                    )
                    processed_count += 1
                    successfully_processed = True

            except Exception as e:
                logger.error(f"Error adding metadata to {image_name}: {e}")
            finally:
                # Ensure backup files are removed regardless of success or failure
                self.remove_backup_file(destination_path)

                # Clean up temp file if it exists and is not needed
                if temp_image_path and os.path.exists(temp_image_path):
                    os.remove(temp_image_path)

            # Remove the original file only if successfully processed and moved
            if successfully_processed and image_path != destination_path:
                os.remove(image_path)

        # Calculate the number of unprocessed images
        unprocessed_count = len(filtered_image_files) - processed_count

        # Display the images processing time
        process_time = time.perf_counter() - time_start

        # Display the processing time of a function
        execution_timer(
            processed_count=processed_count,
            unprocessed_count=unprocessed_count,
            process_time=process_time,
        )

    @staticmethod
    def remove_backup_file(filename):
        """
        Remove the backup file created by the IPTCInfo library.

        Args:
            filename: path to the backup file has a '~' suffix.
        """
        if filename is None or filename.strip() == '':
            logger.error("No valid filename provided to remove backup file.")
            return

        backup_file_path = filename + '~'
        if os.path.exists(backup_file_path):
            try:
                os.remove(backup_file_path)
                logger.warning(f"Removed backup file: {backup_file_path}")
            except Exception as e:
                logger.error(f"Error removing backup file '{backup_file_path}': {e}")

    def __str__(self):
        """
        Return a string representation of the ImagesDescriber instance.

        Returns:
            str: A string representation of the class instance, showing key attributes.
        """
        return (
            f"ImagesDescriber(\n"
            f"\tprompt={self.prompt},\n"
            f"\tsrc_path={self.src_path},\n"
            f"\tdst_path={self.dst_path},\n"
            f"\tauthor_name={self.author_name}\n"
            f")"
        )
