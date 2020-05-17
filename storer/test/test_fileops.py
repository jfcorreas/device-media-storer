import unittest

from storer.fileops import filecopier
from shutil import copyfile
from pathlib import Path

src_files_abs_path = Path().absolute().joinpath('src_files')
dst_files_abs_path = Path().absolute().joinpath('dst_files')

mock_files = []


class TestRenamingFiles(unittest.TestCase):
    def setUp(self):
        copyfile(Path(src_files_abs_path).joinpath('file.txt'),
                 Path(dst_files_abs_path).joinpath('file.txt'))
        mock_files.append(Path(dst_files_abs_path).joinpath('file.txt'))
        copyfile(Path(src_files_abs_path).joinpath('file.txt'),
                 Path(dst_files_abs_path).joinpath('otherfile.txt'))
        mock_files.append(Path(dst_files_abs_path).joinpath('otherfile.txt'))
        copyfile(Path(src_files_abs_path).joinpath('file.txt'),
                 Path(dst_files_abs_path).joinpath('file(1).txt'))
        mock_files.append(Path(dst_files_abs_path).joinpath('file(1).txt'))
        copyfile(Path(src_files_abs_path).joinpath('file.txt'),
                 Path(dst_files_abs_path).joinpath('file'))
        mock_files.append(Path(dst_files_abs_path).joinpath('file'))
        copyfile(Path(src_files_abs_path).joinpath('file.txt'),
                 Path(dst_files_abs_path).joinpath('filefile(1).noextension.txt'))
        mock_files.append(Path(dst_files_abs_path).joinpath('filefile(1).noextension.txt'))

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

    def test_sequential_filename(self):
        self.assertEqual(
            filecopier.sequential_filename(
                Path(dst_files_abs_path).joinpath('otherfile.txt')),
            str(Path(dst_files_abs_path).joinpath('otherfile(1).txt')),
            'File with extension')
        self.assertEqual(
            filecopier.sequential_filename(
                Path(dst_files_abs_path).joinpath('file.txt')),
            str(Path(dst_files_abs_path).joinpath('file(2).txt')),
            'File with extension previously renamed')
        self.assertEqual(
            filecopier.sequential_filename(
                Path(dst_files_abs_path).joinpath('file(1).txt')),
            str(Path(dst_files_abs_path).joinpath('file(1)(1).txt')),
            'File with sequential number in original name')
        self.assertEqual(
            filecopier.sequential_filename(
                Path(dst_files_abs_path).joinpath('file')),
            str(Path(dst_files_abs_path).joinpath('file(1)')),
            'File without extension')
        self.assertEqual(
            filecopier.sequential_filename(
                Path(dst_files_abs_path).joinpath('filefile(1).noextension.txt')),
            str(Path(dst_files_abs_path).joinpath('filefile(1).noextension(1).txt')),
            'File with dots before extension')

    def tearDown(self):
        for f in mock_files:
            Path.unlink(f)
        mock_files.clear()


if __name__ == '__main__':
    unittest.main()
