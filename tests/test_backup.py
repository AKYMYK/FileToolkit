"""
Test cases for backup module.
"""
import os
import tempfile
import unittest
import shutil
from filetoolkit.backup import backup_file, backup_directory
from filetoolkit.exceptions import BackupError, FileNotFoundError

class TestBackup(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.tmpdir, "data.txt")
        with open(self.test_file, 'w') as f:
            f.write("Backup test content")
        self.backup_dir = os.path.join(self.tmpdir, "backups")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_backup_file(self):
        self.assertTrue(backup_file(self.test_file, self.backup_dir))
        files = os.listdir(self.backup_dir)
        self.assertEqual(len(files), 1)
        self.assertIn("data", files[0])

    def test_backup_file_no_timestamp(self):
        backup_file(self.test_file, self.backup_dir, keep_timestamp=False)
        self.assertTrue(os.path.exists(os.path.join(self.backup_dir, "data.txt")))

    def test_backup_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            backup_file("no_file.txt", self.backup_dir)

    def test_backup_directory(self):
        subdir = os.path.join(self.tmpdir, "sub")
        os.makedirs(subdir)
        with open(os.path.join(subdir, "f1.txt"), 'w') as f:
            f.write("test")
        self.assertTrue(backup_directory(subdir, self.backup_dir))
        backups = os.listdir(self.backup_dir)
        self.assertTrue(any(name.startswith("sub_") for name in backups))

if __name__ == '__main__':
    unittest.main()
