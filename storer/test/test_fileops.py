import unittest

from storer.fileops import filecopier


class TestRenamingFiles(unittest.TestCase):

    def test_add_str_to_filename(self):
        self.assertEqual(
            filecopier.add_str_to_filename('file.txt', 'test1'),
            'filetest1.txt')
        self.assertEqual(
            filecopier.add_str_to_filename('file', 'test2'),
            'filetest2')
        self.assertEqual(
            filecopier.add_str_to_filename('file.noextension.txt', 'test3'),
            'file.noextensiontest3.txt')


if __name__ == '__main__':
    unittest.main()
