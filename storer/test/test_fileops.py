import unittest

from storer.fileops import filecopier
from shutil import copyfile
from pathlib import Path


class TestFileOps(unittest.TestCase):
    def setUp(self):
        self.src_files_abs_path = Path().absolute().joinpath('storer').joinpath('test').joinpath('src_files')
        self.dst_files_abs_path = Path().absolute().joinpath('storer').joinpath('test').joinpath('dst_files')

        self.mock_files = []
        copyfile(Path(self.src_files_abs_path).joinpath('file.txt'),
                 Path(self.dst_files_abs_path).joinpath('file.txt'))
        self.mock_files.append(Path(self.dst_files_abs_path).joinpath('file.txt'))
        copyfile(Path(self.src_files_abs_path).joinpath('file.txt'),
                 Path(self.dst_files_abs_path).joinpath('otherfile.txt'))
        self.mock_files.append(Path(self.dst_files_abs_path).joinpath('otherfile.txt'))
        copyfile(Path(self.src_files_abs_path).joinpath('file.txt'),
                 Path(self.dst_files_abs_path).joinpath('file(1).txt'))
        self.mock_files.append(Path(self.dst_files_abs_path).joinpath('file(1).txt'))
        copyfile(Path(self.src_files_abs_path).joinpath('file.txt'),
                 Path(self.dst_files_abs_path).joinpath('file'))
        self.mock_files.append(Path(self.dst_files_abs_path).joinpath('file'))
        copyfile(Path(self.src_files_abs_path).joinpath('file.txt'),
                 Path(self.dst_files_abs_path).joinpath('filefile(1).noextension.txt'))
        self.mock_files.append(Path(self.dst_files_abs_path).joinpath('filefile(1).noextension.txt'))

        copyfile(Path(self.src_files_abs_path).joinpath('file.txt'),
                 Path(self.dst_files_abs_path).joinpath('othername.txt'))
        self.mock_files.append(Path(self.dst_files_abs_path).joinpath('othername.txt'))
        copyfile(Path(self.src_files_abs_path).joinpath('file.txt'),
                 Path(self.dst_files_abs_path).joinpath('distinctfile.txt'))
        self.mock_files.append(Path(self.dst_files_abs_path).joinpath('distinctfile.txt'))

    def tearDown(self):
        for f in self.mock_files:
            Path.unlink(f)
        self.mock_files.clear()


class TestRenamingFiles(TestFileOps):

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
                Path(self.dst_files_abs_path).joinpath('otherfile.txt')),
            str(Path(self.dst_files_abs_path).joinpath('otherfile(1).txt')),
            'File with extension')
        self.assertEqual(
            filecopier.sequential_filename(
                Path(self.dst_files_abs_path).joinpath('file.txt')),
            str(Path(self.dst_files_abs_path).joinpath('file(2).txt')),
            'File with extension previously renamed')
        self.assertEqual(
            filecopier.sequential_filename(
                Path(self.dst_files_abs_path).joinpath('file(1).txt')),
            str(Path(self.dst_files_abs_path).joinpath('file(1)(1).txt')),
            'File with sequential number in original name')
        self.assertEqual(
            filecopier.sequential_filename(
                Path(self.dst_files_abs_path).joinpath('file')),
            str(Path(self.dst_files_abs_path).joinpath('file(1)')),
            'File without extension')
        self.assertEqual(
            filecopier.sequential_filename(
                Path(self.dst_files_abs_path).joinpath('filefile(1).noextension.txt')),
            str(Path(self.dst_files_abs_path).joinpath('filefile(1).noextension(1).txt')),
            'File with dots before extension')


class TestIsTheSameFile(TestFileOps):

    def test_is_the_same_file(self):
        self.assertEqual(
            filecopier.is_the_same_file(
                Path(self.src_files_abs_path).joinpath('file.txt'),
                Path(self.dst_files_abs_path).joinpath('file.txt')),
            True,
            'File with same name and same content an stats')
        self.assertEqual(
            filecopier.is_the_same_file(
                Path(self.src_files_abs_path).joinpath('file.txt'),
                Path(self.dst_files_abs_path).joinpath('othername.txt')),
            True,
            'File with same content an stats but distinct name')
        self.assertEqual(
            filecopier.is_the_same_file(
                Path(self.src_files_abs_path).joinpath('distinctfile.txt'),
                Path(self.dst_files_abs_path).joinpath('distinctfile.txt')),
            False,
            'File with same name but distinct content an stats')


class TestCopyFileByBlocks(TestFileOps):

    def test_copyfile_by_blocks(self):
        filecopier.copyfile_by_blocks(
            Path(self.src_files_abs_path).joinpath('file.txt'),
            Path(self.dst_files_abs_path).joinpath('file_16384.txt')
        )
        filecopier.copyfile_by_blocks(
            Path(self.src_files_abs_path).joinpath('file.txt'),
            Path(self.dst_files_abs_path).joinpath('file_8192.txt'),
            8192
        )

        self.assertEqual(
            filecopier.is_the_same_file(
                Path(self.src_files_abs_path).joinpath('file.txt'),
                Path(self.dst_files_abs_path).joinpath('file_16384.txt')),
            True,
            'File with default block size: 16384')
        self.assertEqual(
            filecopier.is_the_same_file(
                Path(self.src_files_abs_path).joinpath('file.txt'),
                Path(self.dst_files_abs_path).joinpath('file_8192.txt')),
            True,
            'File with block size of 8192')

        Path.unlink(Path(self.dst_files_abs_path).joinpath('file_16384.txt'))
        Path.unlink(Path(self.dst_files_abs_path).joinpath('file_8192.txt'))


if __name__ == '__main__':
    unittest.main()
