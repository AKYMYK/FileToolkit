"""
Simple file backup module.
"""
import os
import shutil
from datetime import datetime
from .utils import is_file_safe, is_dir_safe
from .exceptions import BackupError, FileNotFoundError

def backup_file(file_path: str, backup_dir: str = './backup',
                keep_timestamp: bool = True) -> bool:
    """
    Create a backup copy of a file in the specified directory.
    If keep_timestamp is True, filename will include the current date/time.
    """
    if not is_file_safe(file_path):
        raise FileNotFoundError(f"Source file not accessible: {file_path}")
    os.makedirs(backup_dir, exist_ok=True)

    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    if keep_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_name = f"{name}_{timestamp}{ext}"
    else:
        dest_name = base_name

    dest_path = os.path.join(backup_dir, dest_name)
    try:
        shutil.copy2(file_path, dest_path)
        return True
    except Exception as e:
        raise BackupError(f"Backup failed: {e}")

def backup_directory(dir_path: str, backup_dir: str = './backup',
                     keep_timestamp: bool = True) -> bool:
    """
    Copy an entire directory into backup_dir. Timestamp can be added to the folder name.
    """
    if not is_dir_safe(dir_path):
        raise FileNotFoundError(f"Directory not accessible: {dir_path}")
    os.makedirs(backup_dir, exist_ok=True)

    base_name = os.path.basename(dir_path.rstrip('/\\'))
    if keep_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_name = f"{base_name}_{timestamp}"
    else:
        dest_name = base_name

    dest_path = os.path.join(backup_dir, dest_name)
    try:
        shutil.copytree(dir_path, dest_path)
        return True
    except Exception as e:
        raise BackupError(f"Directory backup failed: {e}")
