"""
File encryption and decryption module using AES.
"""
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def _get_key(user_key: str) -> bytes:
    """Derive a 16-byte key from user input using SHA256."""
    return hashlib.sha256(user_key.encode()).digest()[:16]

def encrypt_file(input_path: str, output_path: str, password: str) -> bool:
    """Encrypt a file with AES-CBC, write to output_path."""
    try:
        key = _get_key(password)
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open(input_path, 'rb') as f:
            plaintext = f.read()
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        with open(output_path, 'wb') as f:
            f.write(iv + ciphertext)
        return True
    except Exception as e:
        print(f"Encryption failed: {e}")
        return False

def decrypt_file(input_path: str, output_path: str, password: str) -> bool:
    """Decrypt a file encrypted with encrypt_file."""
    try:
        key = _get_key(password)
        with open(input_path, 'rb') as f:
            iv = f.read(16)
            ciphertext = f.read()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        with open(output_path, 'wb') as f:
            f.write(plaintext)
        return True
    except Exception as e:
        print(f"Decryption failed: {e}")
        return False
