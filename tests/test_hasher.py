"""
Test cases for hasher module.
"""
import os
import tempfile
import unittest
from filetoolkit.hasher import compute_hash, verify_hash, hash_multiple_files
from filetoolkit.exceptions import FileNotFoundError, HashError

class TestHasher(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.gettempdir()
        self.test_file = os.path.join(self.tmpdir, "hash_test.txt")
        with open(self.test_file, 'w') as f:
            f.write("Hello, Hashing World!" * 20)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_compute_sha256(self):
        h = compute_hash(self.test_file, 'sha256')
        self.assertEqual(len(h), 64)  # SHA256 hex is 64 chars

    def test_compute_md5(self):
        h = compute_hash(self.test_file, 'md5')
        self.assertEqual(len(h), 32)

    def test_verify_correct_hash(self):
        h = compute_hash(self.test_file, 'sha256')
        self.assertTrue(verify_hash(self.test_file, h, 'sha256'))

    def test_verify_incorrect_hash(self):
        self.assertFalse(verify_hash(self.test_file, '0'*64, 'sha256'))

    def test_invalid_algorithm(self):
        with self.assertRaises(HashError):
            compute_hash(self.test_file, 'crc32')

    def test_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            compute_hash("nonexist.txt")

    def test_hash_multiple_files(self):
        tmp2 = os.path.join(self.tmpdir, "hash_test2.txt")
        with open(tmp2, 'w') as f:
            f.write("Another file")
        results = hash_multiple_files([self.test_file, tmp2])
        self.assertEqual(len(results), 2)
        os.remove(tmp2)

if __name__ == '__main__':
    unittest.main()
