"""This module describes images using OpenAI's GPT model."""

import base64
from typing import Optional

import requests
import sys

from src.data.path_manager import get_data_file_path
from src.services.logging_config import setup_logger

# Initialize logger using the setup function
logger = setup_logger(__name__)


def process_photo(image_file, prompt, image_caption: Optional[str] = None):
    """
    Process a given photo to generate a title, description, and keywords with ChatGPT-4.

    Args:
        image_file (file object): The image file to be processed.
        prompt (str): The prompt to be sent to the GPT model for generating descriptions.
        image_caption (Optional[str]): The caption from image metadata, if available.

    Returns:
         dict: A JSON object containing the generated title, description, and keywords.
    """
    # Set your OpenAI API key
    try:
        with open(get_data_file_path('openai_key.txt'), 'r') as f:
            line = f.read()
            API_KEY = line.split('; ')[1].strip()
    except FileNotFoundError as e:
        logger.critical(
            f"Could not find {e.filename}. Please ensure the file exists and is accessible."
        )
        # Exit the program with a status code 1
        sys.exit(1)
    except Exception:
        logger.critical("Error occurred while reading the OpenAI API Key.")
        # Exit the program with a status code 1
        sys.exit(1)

    # Convert the image to a based64 string
    image_base64 = base64.b64encode(image_file.read()).decode('ascii')

    # Create a general prompt for ChatGPT
    if image_caption:
        gen_prompt = (
            f"{prompt}. Use the following context to enhance your response: {image_caption}"
        )
    else:
        gen_prompt = prompt

    # Use GPT-4 by creating a prompt to generate a title, description, and keywords
    payload = {
        'model': 'gpt-4o',
        'messages': [
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': gen_prompt},
                    {
                        'type': 'image_url',
                        'image_url': {'url': f"data:image/jpeg;base64,{image_base64}"},
                    },
                ],
            }
        ],
        'max_tokens': 300,
    }

    response = requests.post(
        url="https://api.openai.com/v1/chat/completions",
        headers={
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {API_KEY}",
        },
        json=payload,
    ).json()

    return response
