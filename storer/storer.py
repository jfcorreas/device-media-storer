import filecmp
from os import scandir
from os.path import isfile, join
from codetiming import Timer                # https://github.com/realpython/codetiming

SOURCE_PATH = "/home/jfcm02/Proyectos/Desarrollo/TestData/source_files"
DESTINATION_PATH = "/home/jfcm02/Proyectos/Desarrollo/TestData/dest_files"


def copyfile_by_blocks(src, dst, block=16384):
    """
    Copies a file from source to destination.

    :param src: source file path
    :type src: str
    :param dst: destination file path
    :type dst: str
    :param block: size of the blocks for the copy iterations
    """
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            for x in iter(lambda: fsrc.read(block), ""):
                if not x:
                    break
                fdst.write(x)


def is_the_same_file(f1, f2):
    """
    Verify if two files are the same file.

    :param f1: path of file 1 for comparison
    :type f1: str
    :param f2: path of file 2 for comparison
    :type f2: str
    :return: True if the file src and the file dst are the same file (content and stats).
     If not return False
    :rtype: bool
    """
    return filecmp.cmp(f1, f2, False) & filecmp.cmp(f1, f2, True)


def add_str_to_filename(f, s):
    """
    Inserts a string into a filename just before the extension. If the filename has no
    extension, the string is inserted at the end of filename.

    :param f: the filename
    :type: str
    :param s: the string to insert
    :type: str
    :return: the filename with the string inserted
    :rtype: str
    """
    extension_index = f.rfind('.')
    flist = list(f)
    if extension_index > -1:
        flist.insert(extension_index, s)
    else:
        flist.insert(len(f), s)
    return "".join(flist)


def rename_file(f):
    """
    Rename a file to avoid name conflicts

    :param f: path of file to rename
    :type: str
    :return: the new name (complete path) of the file
    :rtype: str
    """
    ncopy = 1
    new_name = add_str_to_filename(f, "(" + str(ncopy) + ")")
    while isfile(new_name):
        ncopy += 1
        new_name = add_str_to_filename(f, "(" + str(ncopy) + ")")
    return new_name


class CopyTask:
    """
    Do a file copy tasks and store the results.
    Prevents multiple executions of the copy task.
    """
    def __init__(self, srcdir, dstdir):
        self.srcdir = srcdir
        self.dstdir = dstdir
        self.executed = False
        self.skippedfiles = 0
        self.renamedfiles = 0
        self.copiedfiles = 0
        self.copiedsize = 0
        # https://www.python.org/dev/peps/pep-0471/  @scandir
        self.sourcefiles = [f for f in scandir(SOURCE_PATH) if f.is_file()]
        self.totalsize = sum(f.stat().st_size for f in self.sourcefiles if f.is_file())

    def __repr__(self):     # TODO add more information
        return "Task for copy files from {} to {}".format(self.srcdir, self.dstdir)

    def copy_all_files(self):
        """
        Copy all the files defined in the task

        :return: the number of files copied. If the copy already was executed, returns -1
        """
        if not self.executed:
            self.executed = True
            for f in self.sourcefiles:
                srcfile = f.path
                dstfile = join(DESTINATION_PATH, f.name)
                if isfile(dstfile):
                    if is_the_same_file(srcfile, dstfile):
                        self.skippedfiles += 1
                    else:
                        dstfile = rename_file(dstfile)
                        copyfile_by_blocks(srcfile, dstfile)
                        self.copiedsize += f.stat().st_size
                        self.renamedfiles += 1
                        self.copiedfiles += 1
                else:
                    copyfile_by_blocks(srcfile, dstfile)
                    self.copiedsize += f.stat().st_size
                    self.copiedfiles += 1
            return self.copiedfiles
        else:
            return -1


# filecmp.dircmp(SOURCE_PATH,DESTINATION_PATH).report()

copia1 = CopyTask(SOURCE_PATH, DESTINATION_PATH)
print(copia1)
print(r"Número de Ficheros en {} = {}".format(SOURCE_PATH, len(copia1.sourcefiles)))
print("Tamaño total: {:.2f}MBs".format(round(copia1.totalsize/1024/1024, 2)))
print("Copiando...")
t = Timer(name="class", logger=None)
t.start()
copia1.copy_all_files()
elapsed_time = t.stop()
print("Ficheros con mismo nombre pero distintos (renombrar): {}".format(copia1.renamedfiles))
print("Ficheros idénticos (saltar): {}".format(copia1.skippedfiles))
print("Ficheros copiados: {} (tamaño: {:.2f}MBs)".format(copia1.copiedfiles, round(copia1.copiedsize/1024/1024, 2)))
print("Tiempo transcurrido: {:.4f} segundos".format(round(elapsed_time, 4)))

