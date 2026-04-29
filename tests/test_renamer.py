"""
Test cases for renamer module.
"""
import os
import tempfile
import unittest
from filetoolkit.renamer import preview_rename, batch_rename

class TestRenamer(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Create some dummy files
        for i in range(5):
            fname = f"file{i}.txt"
            with open(os.path.join(self.tmpdir, fname), 'w') as f:
                f.write("dummy")

    def tearDown(self):
        for f in os.listdir(self.tmpdir):
            os.remove(os.path.join(self.tmpdir, f))
        os.rmdir(self.tmpdir)

    def test_preview(self):
        changes = preview_rename(self.tmpdir, prefix="new_")
        self.assertEqual(len(changes), 5)
        for old, new in changes:
            self.assertTrue(new.startswith("new_"))

    def test_batch_rename_with_prefix(self):
        self.assertTrue(batch_rename(self.tmpdir, prefix="p_"))
        files = sorted(os.listdir(self.tmpdir))
        for f in files:
            self.assertTrue(f.startswith("p_"))

    def test_batch_rename_preview_mode(self):
        # Should not actually rename files
        original_files = sorted(os.listdir(self.tmpdir))
        result = batch_rename(self.tmpdir, prefix="x_", preview=True)
        self.assertTrue(result)
        after_files = sorted(os.listdir(self.tmpdir))
        self.assertEqual(original_files, after_files)

    def test_batch_rename_with_replace(self):
        batch_rename(self.tmpdir, replace_old="file", replace_new="doc")
        files = sorted(os.listdir(self.tmpdir))
        for f in files:
            self.assertIn("doc", f)

if __name__ == '__main__':
    unittest.main()
