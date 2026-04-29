"""
Test cases for converter module.
"""
import os
import tempfile
import unittest
from filetoolkit.converter import detect_encoding, convert_encoding

class TestConverter(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.gettempdir()
        self.source = os.path.join(self.tmpdir, "source_gbk.txt")
        self.target = os.path.join(self.tmpdir, "target_utf8.txt")
        # Create a GBK encoded file
        content = "你好，世界！"  # Chinese characters
        with open(self.source, 'w', encoding='gbk') as f:
            f.write(content)

    def tearDown(self):
        for p in [self.source, self.target]:
            if os.path.exists(p):
                os.remove(p)

    def test_detect_encoding(self):
        enc = detect_encoding(self.source)
        self.assertIn(enc.lower(), ['gb2312', 'gbk', 'gb18030'])

    def test_convert_to_utf8(self):
        self.assertTrue(convert_encoding(self.source, self.target,
                                         from_enc='gbk', to_enc='utf-8'))
        with open(self.target, 'r', encoding='utf-8') as f:
            result = f.read()
        self.assertEqual(result, "你好，世界！")

    def test_convert_auto_detect(self):
        # Without specifying source encoding, should auto-detect
        self.assertTrue(convert_encoding(self.source, self.target,
                                         to_enc='utf-8'))
        self.assertTrue(os.path.exists(self.target))

if __name__ == '__main__':
    unittest.main()
