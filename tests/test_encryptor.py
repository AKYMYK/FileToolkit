"""
Test cases for encryptor module.
"""
import os
import tempfile
import unittest
from filetoolkit.encryptor import encrypt_file, decrypt_file

class TestEncryptor(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.gettempdir()
        self.plain = os.path.join(self.tmpdir, "test_plain.txt")
        self.enc = os.path.join(self.tmpdir, "test_enc.enc")
        self.dec = os.path.join(self.tmpdir, "test_dec.txt")
        with open(self.plain, 'w') as f:
            f.write("Hello, FileToolkit!" * 10)

    def tearDown(self):
        for p in [self.plain, self.enc, self.dec]:
            if os.path.exists(p):
                os.remove(p)

    def test_encrypt_decrypt_roundtrip(self):
        self.assertTrue(encrypt_file(self.plain, self.enc, "mypassword"))
        self.assertTrue(os.path.exists(self.enc))
        self.assertTrue(decrypt_file(self.enc, self.dec, "mypassword"))
        with open(self.dec, 'r') as f:
            dec_content = f.read()
        with open(self.plain, 'r') as f:
            plain_content = f.read()
        self.assertEqual(dec_content, plain_content)

    def test_decrypt_wrong_password(self):
        encrypt_file(self.plain, self.enc, "correct")
        result = decrypt_file(self.enc, self.dec, "wrong")
        # Should print error and return False
        self.assertFalse(result)

    def test_encrypt_nonexistent_file(self):
        result = encrypt_file("nonexist.txt", self.enc, "pw")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
