"""
Constants and default values used throughout FileToolkit.
"""

DEFAULT_CHUNK_SIZE = 4096          # 4 KB
DEFAULT_ENCODING = 'utf-8'
DEFAULT_SPLIT_SIZE = 1024 * 1024   # 1 MB
DEFAULT_BACKUP_DIR = './backup'

SUPPORTED_HASH_ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512']
SUPPORTED_CIPHER_MODES = ['CBC']

VERSION = '1.0.0'
AUTHOR = 'FileToolkit Contributors'
