"""Main script to execute the image description and metadata generation project."""

import logging
import threading
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, font, messagebox

from src.csv_generator import CSVGenerator
from src.data.path_manager import get_data_file_path
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

        # Get screen dimensions
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Define default fonts for the application
        self.default_font = font.Font(
            family="Verdana",
            size=int(self.screen_height * 0.015),  # 1,5% of screen height
        )
        self.bold_font = font.Font(
            family="Verdana",
            size=int(self.screen_height * 0.018),  # 1,8% of screen height
            weight="bold",
        )

        # Initialize variables to track the windows
        self.app_settings_window = None
        self.add_metadata_window = None
        self.generate_csv_window = None
        self.processing_status_window = None

        # Open main window
        self._create_main_window()

        # Bind the confirm_close_app method to the app close
        self.root.protocol('WM_DELETE_WINDOW', self.confirm_close_app)

    def _create_main_window(self):
        """
        Open main window.

        This window opens with app starting and allow users to choose options.
        """
        # Set the main window size and place it in the center of the screen
        window_width = int(self.screen_width * 0.4)  # 40% of screen width
        window_height = int(self.screen_height * 0.4)  # 40% of screen height

        x = (self.screen_width // 2) - (window_width // 2)
        y = (self.screen_height // 2) - (window_height // 2)

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Frame to hold the settings button at the top right
        top_frame = tk.Frame(self.root)
        top_frame.pack(side='top', fill='x', padx=10, pady=10)

        # Create a frame for the main buttons and center it
        button_frame = tk.Frame(self.root)
        button_frame.pack(expand=True)

        # Create "Settings" button
        tk.Button(
            top_frame,
            text='Settings',
            font=self.default_font,
            command=self._create_app_settings_window,
        ).pack(side='right')

        # Create "Add Metadata" button
        tk.Button(
            button_frame,
            text='Add Metadata',
            font=self.bold_font,
            height=2,
            width=30,
            command=self._create_add_metadata_window,
        ).pack(pady=10, expand=True)

        # Create "Generate CSV" button
        tk.Button(
            button_frame,
            text='Generate CSV',
            font=self.bold_font,
            height=2,
            width=30,
            command=self._create_generate_csv_window,
        ).pack(pady=10, expand=True)

    def _create_app_settings_window(self):
        """
        Open the application settings window for SmartVisionAI.

        This window allow users to configure the application settings.
        """
        title = 'SmartVisionAI Settings'
        description = "Set up all necessary SmartVisionAI application configurations"

        # If the window doesn't exist, create it
        if self.app_settings_window is None or not tk.Toplevel.winfo_exists(
            self.app_settings_window
        ):
            self.app_settings_window = tk.Toplevel(self.root)
            self.app_settings_window.title(title)

            # Set window size proportional to the screen
            window_width = int(self.screen_width * 0.4)  # 40% of screen width
            window_height = int(self.screen_height * 0.35)  # 35% of screen height
            self.app_settings_window.geometry(f'{window_width}x{window_height}')

            # Labels and entries for title and description
            tk.Label(
                self.app_settings_window,
                text=title,
                font=self.bold_font,
            ).pack(pady=10)
            tk.Label(
                self.app_settings_window,
                text=description,
                font=self.default_font,
                wraplength=400,
                justify='center',
            ).pack(pady=10)

            # OpenAI API Key label and entry
            self.openai_key_entry = tk.Entry(self.app_settings_window, width=40)
            tk.Label(
                self.app_settings_window,
                text='OpenAI API Key',
                font=self.default_font,
            ).pack(pady=(10, 0))
            self.openai_key_entry.pack(pady=10)

            # Display last OpenAI API key info
            last_updated = self.get_openai_key_date()
            tk.Label(
                self.app_settings_window,
                text=last_updated,
                font=font.Font(family='Verdana', size=10, slant='italic'),
            ).pack()

            # Save button
            tk.Button(
                self.app_settings_window,
                text='SAVE',
                font=self.bold_font,
                background='green',
                width=15,
                command=self.save_app_settings,
            ).pack(pady=20)

        else:
            # If the window already exists, lift it to the front
            self.app_settings_window.lift()
            self.app_settings_window.focus_force()

    def _create_add_metadata_window(self):
        """
        Open the window for adding metadata to images.

        This window allows users to describe images and add metadata (title, description, keywords,
         and author name) directly to the image files in a selected folder.
        """
        title = 'Add Metadata'
        description = (
            "Describe all images in the source folder using ChatGPT, "
            "add metadata (title, description, keywords, and author name) directly to "
            "the image files, and save them in the destination folder."
        )

        # If the window doesn't exist, create it
        if self.add_metadata_window is None or not tk.Toplevel.winfo_exists(
            self.add_metadata_window
        ):
            self.add_metadata_window = tk.Toplevel(self.root)
            self.add_metadata_window.title(title)

            # Set window size proportional to the screen
            window_width = int(self.screen_width * 0.4)  # 40% of screen width
            window_height = max(
                650, int(self.screen_height * 0.65)
            )  # At least 650px or 65% of screen height
            self.add_metadata_window.geometry(f'{window_width}x{window_height}')

            # Labels and entries for title and description
            tk.Label(
                self.add_metadata_window,
                text=title,
                font=self.bold_font,
            ).pack(pady=10)
            tk.Label(
                self.add_metadata_window,
                text=description,
                font=self.default_font,
                wraplength=400,
                justify="center",
            ).pack(pady=10)

            # Entry for prompt input with scrollable Text widget
            self.prompt_entry = tk.Text(self.add_metadata_window, width=45, height=8, wrap="word")
            tk.Label(
                self.add_metadata_window,
                text="Prompt",
                font=self.default_font,
            ).pack(pady=(10, 0))
            self.prompt_entry.pack(pady=10)

            # Load the last saved prompt message
            self.get_prompt_message()

            # Scrollbar for the Text widget
            scrollbar = tk.Scrollbar(self.add_metadata_window, command=self.prompt_entry.yview)
            self.prompt_entry.config(yscrollcommand=scrollbar.set)

            # Folder selection buttons for source and destination
            self.src_folder_path = tk.StringVar()
            tk.Button(
                self.add_metadata_window,
                text="Select Source Folder",
                font=self.default_font,
                command=self.select_src_folder,
                width=25,
            ).pack(pady=7)
            tk.Label(
                self.add_metadata_window,
                font=self.default_font,
                textvariable=self.src_folder_path,
            ).pack()

            self.dst_folder_path = tk.StringVar()
            tk.Button(
                self.add_metadata_window,
                text="Select Destination Folder",
                font=self.default_font,
                command=self.select_dst_folder,
                width=25,
            ).pack(pady=7)
            tk.Label(
                self.add_metadata_window,
                font=self.default_font,
                textvariable=self.dst_folder_path,
            ).pack()

            self.author_entry = tk.Entry(self.add_metadata_window, width=40)
            tk.Label(
                self.add_metadata_window,
                text="Author Name (optional)",
                font=self.default_font,
            ).pack(pady=(10, 0))
            self.author_entry.pack(pady=5)

            # RUN button to initiate the processing
            tk.Button(
                self.add_metadata_window,
                text="RUN",
                font=self.bold_font,
                command=lambda: self.confirm_and_run(self.run_add_metadata),
                width=15,
                background='green',
            ).pack(pady=20)

            # Set the close protocol to save the prompt message when the window closes
            self.add_metadata_window.protocol(
                'WM_DELETE_WINDOW',
                lambda: self.save_prompt_message(current_window=self.add_metadata_window),
            )

        else:
            # If the window already exists, lift it to the front
            self.add_metadata_window.lift()
            self.add_metadata_window.focus_force()

    def _create_generate_csv_window(self):
        """
        Open the window for generating a CSV file from image metadata.

        This window allows users to describe images and generate a CSV file with the image filename,
        titles, descriptions, and keywords, saving it to a selected destination folder.
        """

        title = "Generate CSV"
        description = (
            "Describe all images in the source folder using ChatGPT, "
            "generate a CSV file with the image filename, titles, descriptions,"
            " and keywords, and save the CSV file to the destination folder."
        )

        # If the window doesn't exist, create it
        if self.generate_csv_window is None or not tk.Toplevel.winfo_exists(
            self.generate_csv_window
        ):
            self.generate_csv_window = tk.Toplevel(self.root)  # Create a new top-level window
            self.generate_csv_window.title(title)

            # Set window size proportional to the screen
            window_width = int(self.screen_width * 0.4)  # 40% of screen width
            window_height = max(
                600, int(self.screen_height * 0.6)
            )  # At least 600px or 60% of screen height
            self.generate_csv_window.geometry(f"{window_width}x{window_height}")

            # Labels and entries for title and description
            tk.Label(
                self.generate_csv_window,
                text=title,
                font=self.bold_font,
            ).pack(pady=10)
            tk.Label(
                self.generate_csv_window,
                text=description,
                font=self.default_font,
                wraplength=400,
                justify="center",
            ).pack(pady=10)

            # Entry for prompt input with scrollable Text widget
            self.prompt_entry = tk.Text(self.generate_csv_window, width=45, height=8, wrap="word")
            tk.Label(
                self.generate_csv_window,
                text="Prompt",
                font=self.default_font,
            ).pack(pady=(10, 0))
            self.prompt_entry.pack(pady=10)

            # Load the last saved prompt message
            self.get_prompt_message()

            # Scrollbar for the Text widget
            scrollbar = tk.Scrollbar(self.generate_csv_window, command=self.prompt_entry.yview)
            self.prompt_entry.config(yscrollcommand=scrollbar.set)

            # Folder selection buttons for source and destination
            self.src_folder_path = tk.StringVar()
            tk.Button(
                self.generate_csv_window,
                text="Select Source Folder",
                font=self.default_font,
                command=self.select_src_folder,
                width=25,
            ).pack(pady=7)
            tk.Label(
                self.generate_csv_window,
                font=self.default_font,
                textvariable=self.src_folder_path,
            ).pack()

            self.dst_folder_path = tk.StringVar()
            tk.Button(
                self.generate_csv_window,
                text="Select Destination Folder",
                font=self.default_font,
                command=self.select_dst_folder,
                width=25,
            ).pack(pady=10)
            tk.Label(
                self.generate_csv_window,
                font=self.default_font,
                textvariable=self.dst_folder_path,
            ).pack()

            # RUN button to initiate the processing
            tk.Button(
                self.generate_csv_window,
                text="RUN",
                font=self.bold_font,
                background='green',
                width=15,
                command=lambda: self.confirm_and_run(self.run_generate_csv),
            ).pack(pady=20)

            # Set the close protocol to save the prompt message when the window closes
            self.generate_csv_window.protocol(
                'WM_DELETE_WINDOW',
                lambda: self.save_prompt_message(current_window=self.generate_csv_window),
            )

        else:
            # If the window already exists, lift it to the front
            self.generate_csv_window.lift()
            self.generate_csv_window.focus_force()

    def get_prompt_message(self):
        """
        Load the last saved prompt message from prompt_msg.txt file and display it i the prompt entry widget.

        Raises:
            Exception: Logs an error if an unexpected exception occurs during the file read process.
        """
        try:
            with open(get_data_file_path('prompt_msg.txt'), 'r') as file:
                last_prompt = file.read()
                self.prompt_entry.insert('1.0', last_prompt)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")

    def get_openai_key_date(self):
        """
        Load the last saved OpenAI API Key from openai_key.txt file and display the generated data.

        Returns:
            str: A message indicating the last update date or a default message if no data available.

        Raises:
            Exception: Logs an error if an unexpected exception occurs during the file read process.
        """
        try:
            with open(get_data_file_path('openai_key.txt'), 'r') as file:
                line = file.read()
                date = line.split('; ')[0]
                date_info = f"Last updated OpenAI API Key from {date}"
                return date_info if line else 'No OpenAI API Key available'
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")

    def save_app_settings(self):
        """
        Save the SmartVisionAI app configuration settings.

        Writes the OpenAI API Key by the user to 'openai_key.txt'.
        """
        openai_key = self.openai_key_entry.get().strip()

        if not openai_key:
            messagebox.showerror("Error", "OpenAI API Key is required")

        try:
            with open(get_data_file_path('openai_key.txt'), 'w') as openai_file:
                date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                openai_key_record = f"{date}; {openai_key}"
                openai_file.write(openai_key_record)
            self.app_settings_window.destroy()
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")

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
        prompt = self.prompt_entry.get('1.0', tk.END).strip()
        src_folder = self.src_folder_path.get()
        dst_folder = self.dst_folder_path.get()

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

        # If the window doesn't exist, create it
        if self.processing_status_window is None or not tk.Toplevel.winfo_exists(
            self.processing_status_window
        ):
            self.processing_status_window = tk.Toplevel(self.root)
            self.processing_status_window.title("Processing Status")

            # Set window size proportional to the screen
            window_width = int(self.screen_width * 0.7)  # 70% of screen width
            window_height = int(self.screen_height * 0.4)  # 40% of screen height
            self.processing_status_window.geometry(f"{window_width}x{window_height}")

            # Create a frame to hold the Text and Scrollbar
            frame = tk.Frame(self.processing_status_window)
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
                'CRITICAL': 'red',
            }
            # Configure tags for each log level
            for level, color in text_colors.items():
                if level == 'CRITICAL':
                    log_text.tag_configure(
                        level, foreground=color, font=font.Font(family='Verdana', weight='bold')
                    )
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
        else:
            # If the window already exists, lift it to the front
            self.processing_status_window.lift()
            self.processing_status_window.focus_force()

    def run_add_metadata(self):
        """
        Execute the process of adding metadata to images.

        This method retrieves input values and calls the ImagesDescriber to add metadata
        to the images in the specified folder.
        """
        prompt = self.prompt_entry.get('1.0', tk.END).strip()
        src_folder = self.src_folder_path.get()
        dst_folder = self.dst_folder_path.get()
        author_name = self.author_entry.get() if hasattr(self, 'author_entry') else None

        # Save the current prompt message
        self.save_prompt_message()

        logger.info("Starting Metadata addition...")
        image_describer = ImagesDescriber(
            prompt=prompt, src_path=src_folder, dst_path=dst_folder, author_name=author_name
        )
        image_describer.add_metadata()

    def run_generate_csv(self):
        """
        Execute the process of generating a CSV file from image metadata.

        This method retrieves input values and calls the CSVGenerator to write the image metadata to a CSV file.
        """
        prompt = self.prompt_entry.get('1.0', tk.END).strip()
        src_folder = self.src_folder_path.get()
        dst_folder = self.dst_folder_path.get()

        # Save the current prompt message
        self.save_prompt_message()

        logger.info("Starting CSV generation...")
        csv_generator = CSVGenerator(prompt=prompt, src_path=src_folder, dst_path=dst_folder)
        csv_generator.write_data_to_csv()

    def save_prompt_message(self, current_window=None):
        """
        Save the current prompt message to prompt_msg.txt file and optionally close the specified window.

        Attributes:
            current_window (tk.Toplevel, optional): The currently open app window. Defaults to None.

        Raises:
            Exception: Logs an error if an unexpected exception occurs during the file write process.
        """
        try:
            with open(get_data_file_path('prompt_msg.txt'), 'w') as file:
                file.write(self.prompt_entry.get('1.0', tk.END).strip())
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")

        if current_window:
            current_window.destroy()

    def confirm_close_app(self):
        """
        Show a confirmation dialog before closing the application.
        """
        if messagebox.askokcancel('Quit', "Are you sure you want to exit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartVisionAIApp(root)
    root.mainloop()
