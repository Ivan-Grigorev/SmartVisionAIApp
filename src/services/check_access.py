"""Script to check if an image is locked by any process."""

import os.path
import platform
import subprocess
import time

import psutil

from src.services.logging_config import setup_logger

# Initialize logger using the setup function
logger = setup_logger(__name__)


def normalize_path(filepath):
    """Normalize the file path for consistent comparison."""
    return os.path.normcase(os.path.abspath(filepath))


def terminate_processes_using_file(filepath):
    """
    Terminate all processes that are using a specific file.

    Attributes:
        filepath: Path to the file to check and terminate processes for.
    """
    # Get normalized path
    normalized_path = normalize_path(filepath)

    if platform.system() == 'Darwin':  # macOS
        processes = get_processes_using_file_mac(normalized_path)
    elif platform.system() == 'Windows':
        processes = get_processes_using_file_windows(normalized_path)
    else:
        logger.error("Unsupported operating system.")
        return

    if processes:
        for proc in processes:
            terminate_process(proc['pid'])
            time.sleep(1)  # wait to ensure the process is terminated


def get_processes_using_file_mac(filepath):
    """
    Get a list of processes that have a specific file open using 'lsof' on macOS.

    Attributes:
        filepath: Path to the file to check.

    Returns:
        List of process details with 'pid' and 'name'.
    """
    processes = []
    try:
        # Run the 'lsof' command to find processes using the file
        result = subprocess.check_output(['lsof', filepath], text=True)
        lines = result.splitlines()[1:]  # skip the header line
        for line in lines:
            columns = line.split()
            pid = int(columns[1])
            process_name = columns[0]
            processes.append({'pid': pid, 'name': process_name})
    except subprocess.CalledProcessError as e:
        # Check the return code for no processes found using the file
        if e.returncode == 1:
            logger.debug(f"No processes found using the file {filepath}.")
        else:
            logger.error(f"Failed to check processes using the file: {e}")
    return processes


def get_processes_using_file_windows(filepath):
    """
    Get a list of processes that have a specific file open on Windows using 'psutil'.

    Attributes:
        filepath: Path to the file to check.

    Returns:
        List of process details with 'pid' and 'name'.
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            for file in proc.info['open_files'] or []:
                if file.path.lower() == filepath.lower():
                    processes.append({'pid': proc.info['pid'], 'name': proc.info['name']})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes


def terminate_process(pid):
    """
    Terminate a process by its PID.

    Attributes:
        pid: Process ID (PID) of the process to terminate.
    """
    try:
        process = psutil.Process(pid)
        process.terminate()  # send a terminate signal
        process.wait()  # wait for the process to terminate
        logger.info(f"Terminated process {pid} ({process.name()}) that was using the file.")
    except psutil.NoSuchProcess:
        logger.warning(f"Process {pid} does not exist or is already terminated.")
    except psutil.AccessDenied:
        logger.error(f"Access denied when trying to terminate process {pid}.")
