"""
Test cases for cleaner module.
"""
import os
import tempfile
import unittest
import shutil
from filetoolkit.cleaner import (
    remove_empty_dirs,
    delete_temp_files,
    delete_old_files,
    clean_by_extension
)

class TestCleaner(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Create empty dir
        self.empty_dir = os.path.join(self.tmpdir, "empty")
        os.makedirs(self.empty_dir)
        # Create a temp file
        self.temp_file = os.path.join(self.tmpdir, "test.tmp")
        with open(self.temp_file, 'w') as f:
            f.write("temp")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_remove_empty_dirs_dry_run(self):
        removed = remove_empty_dirs(self.tmpdir, dry_run=True)
        self.assertIn(self.empty_dir, removed)
        self.assertTrue(os.path.exists(self.empty_dir))  # still there

    def test_remove_empty_dirs_real(self):
        removed = remove_empty_dirs(self.tmpdir, dry_run=False)
        self.assertIn(self.empty_dir, removed)
        self.assertFalse(os.path.exists(self.empty_dir))

    def test_delete_temp_files_dry_run(self):
        deleted = delete_temp_files(self.tmpdir, dry_run=True)
        self.assertIn(self.temp_file, deleted)
        self.assertTrue(os.path.exists(self.temp_file))

    def test_delete_temp_files_real(self):
        deleted = delete_temp_files(self.tmpdir, dry_run=False)
        self.assertIn(self.temp_file, deleted)
        self.assertFalse(os.path.exists(self.temp_file))

    def test_clean_by_extension(self):
        deleted = clean_by_extension(self.tmpdir, ['.tmp'], dry_run=True)
        self.assertEqual(len(deleted), 1)
        self.assertTrue(os.path.exists(self.temp_file))

if __name__ == '__main__':
    unittest.main()
