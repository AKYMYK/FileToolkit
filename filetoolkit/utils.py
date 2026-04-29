"""
Utility functions: logging, file validation, and progress display.
"""
import os
import logging

logger = logging.getLogger("filetoolkit")
logger.setLevel(logging.DEBUG)
_ch = logging.StreamHandler()
_ch.setLevel(logging.INFO)
_formatter = logging.Formatter('[%(levelname)s] %(message)s')
_ch.setFormatter(_formatter)
logger.addHandler(_ch)

def is_file_safe(path: str) -> bool:
    """Check if path is a regular file and readable."""
    return os.path.isfile(path) and os.access(path, os.R_OK)

def is_dir_safe(path: str) -> bool:
    """Check if path is a directory and readable."""
    return os.path.isdir(path) and os.access(path, os.R_OK)

def file_size(path: str) -> int:
    """Return file size in bytes, or -1 on error."""
    try:
        return os.path.getsize(path)
    except OSError:
        return -1

def read_file_chunks(path: str, chunk_size: int = 4096):
    """Generator that yields file chunks."""
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def confirm_overwrite(path: str) -> bool:
    """Ask user before overwriting an existing file."""
    if os.path.exists(path):
        ans = input(f"File {path} already exists. Overwrite? (y/N): ")
        return ans.strip().lower() == 'y'
    return True

def set_log_level(verbose: bool):
    """Enable debug logging if verbose is True."""
    _ch.setLevel(logging.DEBUG if verbose else logging.INFO)
