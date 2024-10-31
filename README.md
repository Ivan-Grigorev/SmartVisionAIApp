# SmartVisionAIApp

SmartVisionAIApp is an image metadata processing tool that allows users to add descriptive metadata to image files or generate CSV files containing this information. Using the power of OpenAI's GPT model, this application helps to streamline and automate metadata management for images, making it ideal for projects that require structured image data, such as datasets for machine learning, digital asset management, and more.

## Features

- **Add Metadata**: Automatically generates and embeds descriptive metadata (title, description, keywords) into image files.
- **Generate CSV**: Creates a CSV file containing filenames, titles, descriptions, and keywords for each image.
- **User-Friendly Interface**: Provides an intuitive GUI built with Tkinter.
- **Customizable**: Users can specify custom prompts for image descriptions and optionally add author metadata.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Ivan-Grigorev/SmartVisionAIApp.git
   cd SmartVisionAIApp
   ```

2. **Install Dependencies**
   Make sure all required packages are installed by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Add OpenAI API Key**
   Place your OpenAI API key in a file named `openai_key.txt` in the root directory of the project. This key is essential for accessing GPT model capabilities to describe images. **Note**: Be aware of OpenAI’s request limits and usage quotas, as frequent or large requests can quickly exhaust your rate limits and may incur costs.

4. **Run the Application**
   To start the application, execute:
   ```bash
   python run_app.py
   ```

## Usage

- **Adding Metadata to Images**: Select the "Add Metadata" option to automatically add descriptive metadata to images in a specified folder.
- **Generating a CSV File**: Choose "Generate CSV" to create a CSV with image metadata, which will be saved in the destination folder.
- **Setting Source and Destination Folders**: Both options allow for selecting source and destination folders, with prompts for custom descriptions and optional author attribution.

## Project Structure

```plaintext
SmartVisionAIApp/
├── LICENSE
├── README.md
├── app.log                    # Log file generated during runtime
├── openai_key.txt             # File to store OpenAI API key for image descriptions
├── requirements.txt           # Python dependencies for the project
├── run_app.py                 # Main script to execute the application
└── src/
    ├── __init__.py
    ├── csv_generator.py       # Module for CSV file generation with image metadata
    ├── image_describer.py     # Module for the generation of metadata and its addition to the image
    └── services/
        ├── __init__.py
        ├── chatgpt_responder.py    # Handles interaction with GPT model
        ├── check_access.py         # Checks permissions and access to files
        ├── files_filter.py         # Filters valid image files from a directory
        ├── logging_config.py       # Logging setup for the application
        ├── process_timer.py        # Manages processing time for requests
        └── response_parser.py      # Parses responses from GPT model
```

## License

This project is licensed under the terms of the [LICENSE](./LICENSE).

## Credits

This repository and project were created by [Ivan Grigorev](https://github.com/Ivan-Grigorev). The core image processing functionalities are based on the [GPT Image Describer](https://github.com/Ivan-Grigorev/GPTImageDescriber), designed for educational and personal use.
