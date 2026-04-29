"""
Batch file renaming module.
"""
import os
import re

def preview_rename(folder: str, prefix: str = "", suffix: str = "",
                   replace_old: str = None, replace_new: str = None,
                   regex_pattern: str = None, regex_repl: str = None,
                   start_index: int = 1):
    """Simulate rename and return list of (old_name, new_name)."""
    changes = []
    files = sorted(os.listdir(folder))
    for i, filename in enumerate(files):
        old_path = os.path.join(folder, filename)
        if os.path.isdir(old_path):
            continue
        name, ext = os.path.splitext(filename)
        new_name = name
        if replace_old and replace_new:
            new_name = new_name.replace(replace_old, replace_new)
        if regex_pattern and regex_repl:
            new_name = re.sub(regex_pattern, regex_repl, new_name)
        new_name = f"{prefix}{new_name}{suffix}"
        if start_index > 0:
            new_name = f"{new_name}_{start_index + i}"
        new_filename = new_name + ext
        changes.append((filename, new_filename))
    return changes

def batch_rename(folder: str, prefix: str = "", suffix: str = "",
                 replace_old: str = None, replace_new: str = None,
                 regex_pattern: str = None, regex_repl: str = None,
                 start_index: int = 1, preview: bool = False) -> bool:
    """Rename files in folder. If preview=True, only print changes."""
    changes = preview_rename(folder, prefix, suffix,
                             replace_old, replace_new,
                             regex_pattern, regex_repl, start_index)
    if preview:
        print("=== Preview ===")
        for old, new in changes:
            print(f"{old}  ->  {new}")
        return True
    try:
        for old, new in changes:
            os.rename(os.path.join(folder, old),
                      os.path.join(folder, new))
        print(f"Renamed {len(changes)} files successfully.")
        return True
    except Exception as e:
        print(f"Renaming failed: {e}")
        return False
