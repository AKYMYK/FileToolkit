"""
File splitting and merging module.
"""
import os
import math
from .utils import is_file_safe, file_size, confirm_overwrite
from .exceptions import SplitError, FileNotFoundError
from .constants import DEFAULT_CHUNK_SIZE, DEFAULT_SPLIT_SIZE

def split_by_size(file_path: str, chunk_size: int = DEFAULT_SPLIT_SIZE,
                  output_dir: str = None) -> bool:
    """
    Split a file into multiple parts of given chunk_size (in bytes).
    
    Parts are named: originalname.part0001, originalname.part0002, ...
    """
    if not is_file_safe(file_path):
        raise FileNotFoundError(f"File not accessible: {file_path}")
    if chunk_size <= 0:
        raise SplitError("Chunk size must be positive.")

    base_name = os.path.basename(file_path)
    if output_dir is None:
        output_dir = os.path.dirname(file_path) or '.'
    os.makedirs(output_dir, exist_ok=True)

    total_size = file_size(file_path)
    part_num = 1
    try:
        with open(file_path, 'rb') as f_in:
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk:
                    break
                part_name = f"{base_name}.part{part_num:04d}"
                part_path = os.path.join(output_dir, part_name)
                if not confirm_overwrite(part_path):
                    raise SplitError("User aborted overwrite.")
                with open(part_path, 'wb') as f_out:
                    f_out.write(chunk)
                part_num += 1
        return True
    except Exception as e:
        raise SplitError(f"Failed to split file: {e}")

def split_by_parts(file_path: str, num_parts: int,
                   output_dir: str = None) -> bool:
    """
    Split a file into exactly num_parts parts of roughly equal size.
    """
    if not is_file_safe(file_path):
        raise FileNotFoundError(f"File not accessible: {file_path}")
    if num_parts < 1:
        raise SplitError("Number of parts must be at least 1.")

    total_size = file_size(file_path)
    per_part = math.ceil(total_size / num_parts)
    return split_by_size(file_path, per_part, output_dir)

def merge_files(part_paths: list, output_path: str) -> bool:
    """
    Merge a list of part files into a single output file.
    """
    if not part_paths:
        raise SplitError("No part files provided.")
    if not confirm_overwrite(output_path):
        raise SplitError("User aborted overwrite.")

    try:
        with open(output_path, 'wb') as f_out:
            for part in part_paths:
                if not is_file_safe(part):
                    raise FileNotFoundError(f"Part file missing: {part}")
                with open(part, 'rb') as f_in:
                    while True:
                        chunk = f_in.read(DEFAULT_CHUNK_SIZE)
                        if not chunk:
                            break
                        f_out.write(chunk)
        return True
    except Exception as e:
        raise SplitError(f"Failed to merge files: {e}")
