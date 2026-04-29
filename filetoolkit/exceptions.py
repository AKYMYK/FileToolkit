"""
Custom exceptions for FileToolkit.
"""

class FileToolkitError(Exception):
    """Base exception for all FileToolkit errors."""
    pass

class ToolkitFileNotFoundError(FileToolkitError):
    """Raised when a specified file does not exist."""
    pass

class FilePermissionError(FileToolkitError):
    """Raised when file permissions are insufficient."""
    pass

class EncryptionError(FileToolkitError):
    """Raised when encryption or decryption fails."""
    pass

class EncodingError(FileToolkitError):
    """Raised when encoding detection or conversion fails."""
    pass

class RenameError(FileToolkitError):
    """Raised when batch renaming fails."""
    pass

class SplitError(FileToolkitError):
    """Raised when file splitting or merging fails."""
    pass

class BackupError(FileToolkitError):
    """Raised when backup operation fails."""
    pass

class HashError(FileToolkitError):
    """Raised when hash computation fails."""
    pass
