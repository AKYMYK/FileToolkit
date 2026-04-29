"""
File hashing module: compute MD5, SHA1, SHA256, SHA512.
"""
import hashlib
import os
from .utils import is_file_safe, read_file_chunks
from .exceptions import HashError, FileNotFoundError
from .constants import DEFAULT_CHUNK_SIZE, SUPPORTED_HASH_ALGORITHMS

def compute_hash(file_path: str, algorithm: str = 'sha256') -> str:
    """
    Compute and return the hex digest of a file.
    
    Supported algorithms: md5, sha1, sha256, sha512.
    """
    if algorithm not in SUPPORTED_HASH_ALGORITHMS:
        raise HashError(f"Unsupported algorithm: {algorithm}. "
                        f"Supported: {', '.join(SUPPORTED_HASH_ALGORITHMS)}")
    if not is_file_safe(file_path):
        raise FileNotFoundError(f"File not accessible: {file_path}")

    hash_obj = hashlib.new(algorithm)
    for chunk in read_file_chunks(file_path, DEFAULT_CHUNK_SIZE):
        hash_obj.update(chunk)
    return hash_obj.hexdigest()

def verify_hash(file_path: str, expected_hash: str, algorithm: str = 'sha256') -> bool:
    """
    Verify that the file's hash matches the expected value.
    
    Returns True if they match, False otherwise.
    """
    actual = compute_hash(file_path, algorithm)
    return actual == expected_hash

def hash_multiple_files(file_paths: list, algorithm: str = 'sha256') -> dict:
    """
    Compute hash for multiple files and return a dictionary {path: hash}.
    """
    results = {}
    for path in file_paths:
        try:
            results[path] = compute_hash(path, algorithm)
        except Exception as e:
            results[path] = f"Error: {e}"
    return results
