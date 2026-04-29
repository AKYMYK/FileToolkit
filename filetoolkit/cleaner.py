"""
Directory cleaner module: remove empty dirs, temp files, etc.
"""
import os
import fnmatch
from .utils import is_dir_safe, is_file_safe

def remove_empty_dirs(directory: str, dry_run: bool = True) -> list:
    """
    Find and optionally remove empty sub-directories.
    Returns a list of paths that were (or would be) removed.
    """
    if not is_dir_safe(directory):
        raise ValueError(f"Directory not accessible: {directory}")
    removed = []
    # Bottom-up to remove nested empty dirs
    for root, dirs, files in os.walk(directory, topdown=False):
        if root == directory:
            continue
        if not os.listdir(root):  # empty
            removed.append(root)
            if not dry_run:
                os.rmdir(root)
    return removed

def delete_temp_files(directory: str, dry_run: bool = True,
                      patterns: list = None) -> list:
    """
    Delete temporary files matching given name patterns.
    Default patterns: *.tmp, *.temp, *~, *.bak, *.log
    Returns list of file paths deleted (or would be deleted).
    """
    if not is_dir_safe(directory):
        raise ValueError(f"Directory not accessible: {directory}")
    if patterns is None:
        patterns = ['*.tmp', '*.temp', '*~', '*.bak', '*.log']
    deleted = []
    for root, dirs, files in os.walk(directory):
        for fname in files:
            for pat in patterns:
                if fnmatch.fnmatch(fname, pat):
                    full = os.path.join(root, fname)
                    deleted.append(full)
                    if not dry_run:
                        try:
                            os.remove(full)
                        except OSError:
                            pass
                    break
    return deleted

def delete_old_files(directory: str, days: int = 30,
                     dry_run: bool = True) -> list:
    """
    Delete files older than given number of days (based on modification time).
    Returns list of files that would be/are deleted.
    """
    if not is_dir_safe(directory):
        raise ValueError(f"Directory not accessible: {directory}")
    import time
    now = time.time()
    cutoff = now - (days * 86400)
    deleted = []
    for root, dirs, files in os.walk(directory):
        for fname in files:
            full = os.path.join(root, fname)
            try:
                mtime = os.path.getmtime(full)
                if mtime < cutoff:
                    deleted.append(full)
                    if not dry_run:
                        os.remove(full)
            except OSError:
                pass
    return deleted

def clean_by_extension(directory: str, extensions: list,
                       dry_run: bool = True) -> list:
    """
    Delete all files with specified extensions (e.g. ['.tmp', '.log']).
    """
    if not is_dir_safe(directory):
        raise ValueError(f"Directory not accessible: {directory}")
    deleted = []
    for root, dirs, files in os.walk(directory):
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in extensions:
                full = os.path.join(root, fname)
                deleted.append(full)
                if not dry_run:
                    try:
                        os.remove(full)
                    except OSError:
                        pass
    return deleted
