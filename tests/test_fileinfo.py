"""
Test cases for fileinfo module.
"""
import os
import tempfile
import unittest
import shutil
from filetoolkit.fileinfo import (
    count_files_by_extension,
    total_size_of_directory,
    list_largest_files,
    file_age_summary,
    generate_report
)

class TestFileInfo(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        # Create a few test files
        with open(os.path.join(self.tmpdir, "doc.txt"), 'w') as f:
            f.write("Hello")
        with open(os.path.join(self.tmpdir, "data.csv"), 'w') as f:
            f.write("a,b,c")
        with open(os.path.join(self.tmpdir, "noext"), 'w') as f:
            f.write("no extension")
        sub = os.path.join(self.tmpdir, "subdir")
        os.makedirs(sub)
        with open(os.path.join(sub, "subfile.py"), 'w') as f:
            f.write("print('hey')")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_count_by_extension(self):
        counts = count_files_by_extension(self.tmpdir)
        self.assertEqual(counts.get('.txt'), 1)
        self.assertEqual(counts.get('.csv'), 1)
        self.assertEqual(counts.get('.py'), 1)
        self.assertEqual(counts.get('no_extension'), 1)

    def test_total_size(self):
        size = total_size_of_directory(self.tmpdir)
        self.assertGreater(size, 0)

    def test_largest_files(self):
        top = list_largest_files(self.tmpdir, top_n=2)
        self.assertEqual(len(top), 2)

    def test_file_age_summary(self):
        path = os.path.join(self.tmpdir, "doc.txt")
        info = file_age_summary(path)
        self.assertIn('file', info)
        self.assertEqual(info['size'], 5)

    def test_generate_report(self):
        report = generate_report(self.tmpdir)
        self.assertIn('doc.txt', report)

if __name__ == '__main__':
    unittest.main()
