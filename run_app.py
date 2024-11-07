"""Main script to execute the image description and metadata generation project."""

import logging
import threading
import tkinter as tk
from tkinter import filedialog, font, messagebox

from src.csv_generator import CSVGenerator
from src.image_describer import ImagesDescriber
from src.services.logging_config import TextHandler, setup_logger

# Initialize logger using the setup function
logger = setup_logger(__name__)


class SmartVisionAIApp:
    """
    Main application class for the SmartVisionAI program.

    This class initializes the GUI, sets up main functionality buttons,
    and provides windows for adding metadata to images or generating a CSV
    with image metadata.
    """

    def __init__(self, root):
        """
        Initialize the SmartVisionAI application.

        Attributes:
            root (tk.Tk): The root window for the Tkinter application.
        """
        self.root = root
        self.root.title("SmartVisionAI")  # Set the title of the main window
        self.root.geometry("600x500")  # Set the size of the main window

        # Define default fonts for the application
        self.default_font = font.Font(family="Verdana", size=14)
        self.bold_font = font.Font(family="Verdana", size=16, weight="bold")

        # Create a frame for the main buttons and center it
        button_frame = tk.Frame(self.root)
        button_frame.pack(expand=True)

        # Create "Add Metadata" button
        tk.Button(
            button_frame,
            text="Add Metadata",
            font=self.bold_font,
            height=2,
            width=30,
            command=self.open_add_metadata_window,
        ).pack(pady=10)

        # Create "Generate CSV" button
        tk.Button(
            button_frame,
            text="Generate CSV",
            font=self.bold_font,
            height=2,
            width=30,
            command=self.open_generate_csv_window,
        ).pack(pady=10)

    def open_add_metadata_window(self):
        """
        Open the window for adding metadata to images.

        This window allows users to describe images and add metadata (title, description, and keywords)
        directly to the image files in a selected folder.
        """
        self._create_option_window(
            "Add Metadata",
            "Describe all images in the source folder using ChatGPT,"
            " add metadata (title, description, and keywords) directly to"
            " the image files, and save them in the destination folder.",
            self.run_add_metadata,
            include_author=True,
        )

    def open_generate_csv_window(self):
        """
        Open the window for generating a CSV file from image metadata.

        This window allows users to describe images and generate a CSV file with the image filename,
        titles, descriptions, and keywords, saving it to a selected destination folder.
        """
        self._create_option_window(
            "Generate CSV",
            "Describe all images in the source folder using ChatGPT,"
            " generate a CSV file with the image filename, titles, "
            "descriptions, and keywords, and save the CSV file to the"
            " destination folder.",
            self.run_generate_csv,
            include_author=False,
        )

    def _create_option_window(self, title, description, run_callback, include_author):
        """
        Create a window for selecting options and input fields for metadata or CSV generation.

        Attributes:
            title (str): The title of the option window.
            description (str): A description of the action to be performed.
            run_callback (callable): The function to call when the user clicks the "RUN" button.
            include_author (bool): Whether to include an author name entry in the window.
        """
        window = tk.Toplevel(self.root)  # Create a new top-level window
        window.title(title)
        window.geometry("700x600")

        # Labels and entries for title and description
        tk.Label(window, text=title, font=self.bold_font).pack(pady=10)
        tk.Label(
            window,
            text=description,
            font=self.default_font,
            wraplength=400,
            justify="center",
        ).pack(pady=10)

        # Entry for prompt input with scrollable Text widget
        self.prompt_entry = tk.Text(window, width=45, height=8, wrap="word")
        tk.Label(window, text="Prompt", font=self.default_font).pack(pady=(10, 0))
        self.prompt_entry.pack(pady=10)

        # Scrollbar for the Text widget
        scrollbar = tk.Scrollbar(window, command=self.prompt_entry.yview)
        self.prompt_entry.config(yscrollcommand=scrollbar.set)

        # Folder selection buttons for source and destination
        self.src_folder_path = tk.StringVar()
        tk.Button(
            window,
            text="Select Source Folder",
            font=self.default_font,
            command=self.select_src_folder,
            width=25,
        ).pack(pady=10)
        tk.Label(window, textvariable=self.src_folder_path, fg='white').pack()

        self.dst_folder_path = tk.StringVar()
        tk.Button(
            window,
            text="Select Destination Folder",
            font=self.default_font,
            command=self.select_dst_folder,
            width=25,
        ).pack(pady=10)
        tk.Label(window, textvariable=self.dst_folder_path, fg='white').pack()

        # If author name is required, create an entry for it
        if include_author:
            self.author_entry = tk.Entry(window, width=40)
            tk.Label(window, text="Author Name (optional)", font=self.default_font).pack(
                pady=(10, 0)
            )
            self.author_entry.pack(pady=5)

        # RUN button to initiate the processing
        tk.Button(
            window,
            text="RUN",
            font=self.default_font,
            command=lambda: self.confirm_and_run(run_callback),
        ).pack(pady=20)

    def select_src_folder(self):
        """
        Open a dialog to select the source folder containing images.

        The selected folder path is stored in the src_folder_path variable.
        """
        self.src_folder_path.set(filedialog.askdirectory(title="Select Source Folder"))

    def select_dst_folder(self):
        """
        Open a dialog to select the destination folder for output files.

        The selected folder path is stored in the dst_folder_path variable.
        """
        self.dst_folder_path.set(filedialog.askdirectory(title="Select Destination Folder"))

    def confirm_and_run(self, run_callback):
        """
        Confirm the selected options and run the specified callback function.

        Attributes:
            run_callback (callable): The function to run for processing.
        """
        prompt = self.prompt_entry.get('1.0', tk.END).strip()  # Get the prompt from the text field
        src_folder = self.src_folder_path.get()  # Get the source folder path
        dst_folder = self.dst_folder_path.get()  # Get the destination folder path

        # Check for required fields and show error messages if any are missing
        if not prompt:
            messagebox.showerror("Error", "Prompt is required.")
            return
        if not src_folder:
            messagebox.showerror("Error", "Source folder is required.")
            return

        # Create a confirmation message to show the user
        confirmation_msg = (
            f"Source Folder: {src_folder}\n"
            f"Destination Folder: {dst_folder if dst_folder else 'Not specified'}"
        )
        if src_folder == dst_folder:
            confirmation_msg += "\n\nWarning: Files may be overwritten as source and destination folders are the same."

        # Ask the user for confirmation before proceeding
        if messagebox.askyesno("Confirm", confirmation_msg):
            logger_thread = threading.Thread(target=self.run_with_logger, args=(run_callback,))
            logger_thread.start()

    def run_with_logger(self, run_callback):
        """
        Run the specified callback function and show the logger window.

        Attributes:
            run_callback (callable): The function to run for processing.
        """
        self.show_logger_window()
        run_callback()

    def show_logger_window(self):
        """
        Display a window to show the processing status and log messages.

        The log messages are updated every second by reading from the log file.
        """
        logger_window = tk.Toplevel(self.root)  # Create a new top-level window for logging
        logger_window.title("Processing Status")
        logger_window.geometry("1000x400")

        # Create a frame to hold the Text and Scrollbar
        frame = tk.Frame(logger_window)
        frame.pack(expand=True, fill='both')

        # Create a Text widget for log messages
        log_text = tk.Text(frame, font=self.default_font, bg='black', wrap='word')
        log_text.pack(expand=True, fill='both', side=tk.LEFT)

        # Create a Scrollbar and associate it with the Text widget
        scrollbar = tk.Scrollbar(frame, command=log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        log_text.config(yscrollcommand=scrollbar.set)

        text_colors = {
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'dark red',
        }
        # Configure tags for each log level
        for level, color in text_colors.items():
            log_text.tag_configure(level, foreground=color)

        # Set up TextHandler for live logging in the Text widget
        text_handler = TextHandler(log_text)
        text_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S'
            )
        )

        # Attach the TextHandler to the app logger
        app_logger = setup_logger('root')
        app_logger.addHandler(text_handler)

    def run_add_metadata(self):
        """
        Execute the process of adding metadata to images.

        This method retrieves input values and calls the ImagesDescriber to add metadata
        to the images in the specified folder.
        """
        prompt = self.prompt_entry.get('1.0', tk.END).strip()  # Get the prompt from the text field
        src_folder = self.src_folder_path.get()  # Get the source folder path
        dst_folder = self.dst_folder_path.get()  # Get the destination folder path
        author_name = (
            self.author_entry.get() if hasattr(self, 'author_entry') else None
        )  # Get the author name if present

        logger.info("Starting metadata addition...")
        image_describer = ImagesDescriber(
            prompt=prompt, src_path=src_folder, dst_path=dst_folder, author_name=author_name
        )
        image_describer.add_metadata()

    def run_generate_csv(self):
        """
        Execute the process of generating a CSV file from image metadata.

        This method retrieves input values and calls the CSVGenerator to write the image metadata to a CSV file.
        """
        prompt = self.prompt_entry.get('1.0', tk.END).strip()  # Get the prompt from the text field
        src_folder = self.src_folder_path.get()  # Get the source folder path
        dst_folder = self.dst_folder_path.get()  # Get the destination folder path

        logger.info("Starting CSV generation...")
        csv_generator = CSVGenerator(prompt=prompt, src_path=src_folder, dst_path=dst_folder)
        csv_generator.write_data_to_csv()


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartVisionAIApp(root)
    root.mainloop()
