import unittest
from unittest.mock import patch
import sys
import io
from contextlib import redirect_stdout

from print_files import print_files


class TestPrintFiles(unittest.TestCase):

    def test_one(self):
        with patch.object(sys, 'argv', ['', '../dictionary']):
            with io.StringIO() as buf, redirect_stdout(buf):
                print_files()
                files = buf.getvalue()

        files = files.split('\n')
        files_map = {f.split('\t')[0]: int(f.split('\t')[1]) for f in files if f}
        files_sizes = [int(f.split('\t')[1]) for f in files if f]

        self.assertGreater(files_map['dictionary.py'], 1980)
        self.assertEqual(files_map['output.txt'], 115)
        self.assertEqual(files_map['input.txt'], 82)
        self.assertEqual(files_sizes, sorted(files_sizes, reverse=True))


if __name__ == "__main__":
    unittest.main()
