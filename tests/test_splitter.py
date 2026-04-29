"""
Test cases for splitter module.
"""
import os
import tempfile
import unittest
from filetoolkit.splitter import split_by_size, split_by_parts, merge_files
from filetoolkit.exceptions import SplitError, FileNotFoundError

class TestSplitter(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.source = os.path.join(self.tmpdir, "bigfile.bin")
        # Create a 10000-byte dummy file
        with open(self.source, 'wb') as f:
            f.write(b'A' * 10000)

    def tearDown(self):
        for f in os.listdir(self.tmpdir):
            os.remove(os.path.join(self.tmpdir, f))
        os.rmdir(self.tmpdir)

    def test_split_by_size(self):
        out_dir = os.path.join(self.tmpdir, 'parts')
        self.assertTrue(split_by_size(self.source, 3000, out_dir))
        parts = sorted(os.listdir(out_dir))
        self.assertEqual(len(parts), 4)  # 10000/3000 -> 4 parts
        # Merge and verify
        merged = os.path.join(self.tmpdir, 'merged.bin')
        part_paths = [os.path.join(out_dir, p) for p in parts]
        self.assertTrue(merge_files(part_paths, merged))
        with open(self.source, 'rb') as f1, open(merged, 'rb') as f2:
            self.assertEqual(f1.read(), f2.read())

    def test_split_by_parts(self):
        out_dir = os.path.join(self.tmpdir, 'parts2')
        self.assertTrue(split_by_parts(self.source, 5, out_dir))
        parts = sorted(os.listdir(out_dir))
        self.assertEqual(len(parts), 5)

    def test_merge_wrong_order(self):
        out_dir = os.path.join(self.tmpdir, 'parts3')
        split_by_parts(self.source, 3, out_dir)
        parts = sorted(os.listdir(out_dir))
        # Reverse order and merge should not match original
        part_paths = [os.path.join(out_dir, p) for p in reversed(parts)]
        merged = os.path.join(self.tmpdir, 'merged_rev.bin')
        merge_files(part_paths, merged)
        with open(self.source, 'rb') as f1, open(merged, 'rb') as f2:
            self.assertNotEqual(f1.read(), f2.read())

if __name__ == '__main__':
    unittest.main()
