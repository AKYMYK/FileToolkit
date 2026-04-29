"""
File information and statistics module.
"""
import os
from datetime import datetime
from .utils import is_dir_safe, is_file_safe, human_readable_size

def count_files_by_extension(directory: str) -> dict:
    """
    Recursively count files in directory, grouped by extension.
    Returns a dict: {'.txt': 5, '.py': 3, ...}
    Extension is lowercased. Files without extension are grouped under 'no_extension'.
    """
    if not is_dir_safe(directory):
        raise ValueError(f"Directory not accessible: {directory}")
    counts = {}
    for root, dirs, files in os.walk(directory):
        for fname in files:
            _, ext = os.path.splitext(fname)
            ext = ext.lower() if ext else 'no_extension'
            counts[ext] = counts.get(ext, 0) + 1
    return counts

def total_size_of_directory(directory: str) -> int:
    """
    Return total size in bytes of all files inside directory (recursive).
    """
    if not is_dir_safe(directory):
        raise ValueError(f"Directory not accessible: {directory}")
    total = 0
    for root, dirs, files in os.walk(directory):
        for fname in files:
            path = os.path.join(root, fname)
            try:
                total += os.path.getsize(path)
            except OSError:
                pass
    return total

def list_largest_files(directory: str, top_n: int = 10) -> list:
    """
    Return list of (path, size_in_bytes) for the top_n largest files.
    """
    if not is_dir_safe(directory):
        raise ValueError(f"Directory not accessible: {directory}")
    files_info = []
    for root, dirs, files in os.walk(directory):
        for fname in files:
            path = os.path.join(root, fname)
            try:
                sz = os.path.getsize(path)
                files_info.append((path, sz))
            except OSError:
                continue
    files_info.sort(key=lambda x: x[1], reverse=True)
    return files_info[:top_n]

def file_age_summary(file_path: str) -> dict:
    """
    Return a dict with creation time, modification time, and age in days.
    """
    if not is_file_safe(file_path):
        raise ValueError(f"File not accessible: {file_path}")
    stat = os.stat(file_path)
    ctime = datetime.fromtimestamp(stat.st_ctime)
    mtime = datetime.fromtimestamp(stat.st_mtime)
    now = datetime.now()
    age_days = (now - mtime).days
    return {
        'file': file_path,
        'created': ctime.strftime('%Y-%m-%d %H:%M:%S'),
        'modified': mtime.strftime('%Y-%m-%d %H:%M:%S'),
        'age_days': age_days,
        'size': stat.st_size,
        'size_human': human_readable_size(stat.st_size)
    }

def generate_report(directory: str) -> str:
    """
    Generate a multi-line text report about directory stats.
    """
    report = []
    report.append(f"Directory Report for: {directory}")
    report.append("=" * 50)
    try:
        total_size = total_size_of_directory(directory)
        report.append(f"Total size: {human_readable_size(total_size)}")
        ext_counts = count_files_by_extension(directory)
        total_files = sum(ext_counts.values())
        report.append(f"Total files: {total_files}")
        report.append("Files by extension:")
        for ext, count in sorted(ext_counts.items()):
            report.append(f"  {ext}: {count}")
        report.append("Top 5 largest files:")
        for path, sz in list_largest_files(directory, top_n=5):
            report.append(f"  {os.path.basename(path)} - {human_readable_size(sz)}")
    except Exception as e:
        report.append(f"Error generating report: {e}")
    return '\n'.join(report)
