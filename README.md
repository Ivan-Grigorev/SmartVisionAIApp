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
├── .gitattributes                  # Git configuration for handling file attributes
├── .gitignore                      # Specifies files and directories to be ignored by Git
├── .pre-commit-config.yaml         # Configuration file for pre-commit hooks
├── builddmg.sh                     # Script to create a disk image for installation
├── LICENSE                         # License information for the project
├── README.md                       # Project documentation
├── requirements.txt                # List of Python dependencies
├── run_app.py                      # Main script to launch the application
└── src/
    ├── __init__.py                 # Marks the src directory as a package
    ├── csv_generator.py            # Generates CSV files with image metadata
    ├── image_describer.py          # Adds metadata to images based on descriptions
    ├── app_icons/
    │   └── smartvisionaiapp.ico    # Icon for the application
    ├── data/
    │   ├── __init__.py             # Marks the data directory as a package
    │   ├── path_manager.py         # Check and creates a path to data files
    │   ├── openai_key.txt          # Stores OpenAI API key
    │   └── prompt_msg.txt          # Stores the user's prompt message
    └── services/
        ├── __init__.py             # Marks the services directory as a package
        ├── chatgpt_responder.py    # Handles interactions with the GPT model
        ├── check_access.py         # Verifies permissions and file access
        ├── files_filter.py         # Filters and validates image files in a directory
        ├── logging_config.py       # Configures logging for the application
        ├── process_timer.py        # Displays processing time
        └── response_parser.py      # Parses and structures responses from the GPT model
```

## Creating a Standalone Executable with PyInstaller

To distribute **SmartVisionAIApp** as a standalone executable, you can use **PyInstaller**, which bundles your Python application and all its dependencies into a single file. 
> [!NOTE]
> Since **PyInstaller** is already included in `requirements.txt`, you don’t need to install it separately.

1. **Create the Executable**
   To create an executable, run the following command in the root directory of the project:
   ```bash
   pyinstaller --name "SmartVisionAI" --onefile --windowed --icon=src/app_icons/smartvisionaiapp.ico \
    --add-data "src/data/openai_key.txt:data" \
    --add-data "src/data/prompt_msg.txt:data" \
    run_app.py
   ```
   Explanation of the options:
   - `--name "SmartVisionAI"`: Sets the name of the executable.
   - `--onefile`: Bundles the app into a single executable file.
   - `--windowed`: Disables the command line window (for GUI apps).
   - `--icon=src/app_icons/smartvisionaiapp.ico`: Adds an icon to the executable (ensure the icon path is correct).
   - `--add-data "src/data/openai_key.txt:data"`: Includes openai_key.txt in the 'data' folder in the bundle.
   - `--add-data "src/data/prompt_msg.txt:data"`: Includes prompt_msg.txt in the 'data' folder in the bundle.

2. **Find the Executable**
   After running the command, the executable will be created in the `dist` directory within your project folder. You can now share or distribute this standalone executable.

### Creating a macOS Disk Image for Installation

To create a macOS disk image for installing **SmartVisionAIApp**, you can use the `builddmg.sh` script included in the project. This script automates the process of creating a `.dmg` file for easy distribution on macOS.

### Steps to Use the `builddmg.sh` Script

1. **Ensure You Have the Necessary Tools**
   Make sure you have **Homebrew** installed and the necessary dependencies like `hdiutil` for macOS. If not, you can install Homebrew by following the instructions at [https://brew.sh/](https://brew.sh/).

2. **Make the Script Executable**
   Open a terminal and navigate to the directory where the `builddmg.sh` file is located. Run the following command to make the script executable:
   ```bash
   chmod +x builddmg.sh
   ```

3. **Run the Script**
   Execute the script with the following command:
   ```bash
   ./builddmg.sh
   ```
   This script will:
   - Build the application into an executable (if not already done).
   - Create a `.dmg` file with the packaged app inside, ready for distribution.

4. **Find the Disk Image**
   After the script finishes, you will find the `.dmg` file in the root project directory. You can now use it for installation on macOS.

### Creating a Windows Executable for Installation

To create a standalone executable for Windows, follow these steps:

1. **Transfer Project to a Windows Environment**:
   Since PyInstaller builds are platform-specific, run the following steps on a Windows system or virtual machine.

2. **Install Python and Dependencies on Windows**:
   - Install Python and ensure it’s added to your system path.
   - In the root project folder, install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the PyInstaller Command on Windows**:
   Run the same PyInstaller command as above to create a Windows-compatible `.exe` file:
   ```bash
   pyinstaller --name "SmartVisionAI" --onefile --windowed --icon=src/app_icons/smartvisionaiapp.ico \
       --add-data "src/data/openai_key.txt;data" \
       --add-data "src/data/prompt_msg.txt;data" \
       run_app.py
   ```
> [!NOTE]
> On Windows, the `--add-data` paths should use a semicolon (`;`) instead of a colon (`:`).

4. **Locate the Executable**:
   After the build completes, you will find `SmartVisionAI.exe` in the `dist` directory. This `.exe` file contains all dependencies and can be distributed directly to Windows users. They can simply double-click the `.exe` to run the app without installing Python.

## License

This project is licensed under the terms of the [LICENSE](./LICENSE).

## Credits

This repository and project were created by [Ivan Grigorev](https://github.com/Ivan-Grigorev). The core image processing functionalities are based on the [GPT Image Describer](https://github.com/Ivan-Grigorev/GPTImageDescriber), designed for educational and personal use.
