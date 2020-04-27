import filecmp
from os import scandir
from os.path import isfile, join
from codetiming import Timer                # https://github.com/realpython/codetiming
from datetime import datetime, timedelta
from tqdm import tqdm
from time import sleep

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
    :type f: str
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
    def __init__(self, srcdir, dstdir, pbar=True):
        self.srcdir = srcdir
        self.dstdir = dstdir
        self.progressbar = pbar
        self.executed = False
        self.skippedfiles = 0
        self.renamedfiles = 0
        self.copiedfiles = 0
        self.copiedsize = 0
        self.selectedsize = 0
        # https://www.python.org/dev/peps/pep-0471/  @scandir
        self.sourcefiles = [f for f in scandir(SOURCE_PATH) if f.is_file()]
        self.totalsize = sum(f.stat().st_size for f in self.sourcefiles)

    def __repr__(self):
        return "Task for copy files from {} to {}".format(self.srcdir, self.dstdir)

    def do_copy(self, from_date=None, to_date=None):
        """
        Copy the files defined in the task

        :param from_date: Optional. Copy source files with last modified date after to from_date
        :type from_date: datetime
        :param to_date: Optional. Copy source files with last modified date previous to to_date
        :type to_date: datetime
        :return: the number of copied files. If the copy already runs, return -1
        """
        if not self.executed:
            self.executed = True
            if from_date or to_date:
                if type(to_date) is datetime:
                    to_date += timedelta(days=1)
                selected_files = []
                for f in self.sourcefiles:
                    mdate = datetime.fromtimestamp(f.stat().st_mtime)
                    if type(from_date) is datetime and type(to_date) is datetime:
                        if from_date <= mdate < to_date:
                            selected_files.append(f)
                    elif type(from_date) is datetime:
                        if from_date <= mdate:
                            selected_files.append(f)
                    elif type(to_date) is datetime:
                        if mdate < to_date:
                            selected_files.append(f)
                    else:
                        raise TypeError("Both optional arguments are invalid dates: "
                                        "from_date={}, to_date={}".format(from_date, to_date))
                return self.__copy_files(selected_files)
            else:
                return self.__copy_files(self.sourcefiles)
        else:
            return -1

    def __copy_files(self, selected_files):
        """
        Private function. Copy the files in selected_files

        :param selected_files: list of files to copy
        :type selected_files: list
        :return: the number of copied files.
        """
        self.selectedsize = sum(f.stat().st_size for f in selected_files)
        with tqdm(total=self.selectedsize, disable=not self.progressbar,
                  desc="Copying files",
                  unit="Byte", unit_scale=True, unit_divisor=1024) as pbar:
            for f in selected_files:
                srcfile = f.path
                dstfile = join(DESTINATION_PATH, f.name)
                if isfile(dstfile):
                    if is_the_same_file(srcfile, dstfile):
                        self.skippedfiles += 1
                        pbar.total -= f.stat().st_size
                    else:
                        dstfile = rename_file(dstfile)
                        copyfile_by_blocks(srcfile, dstfile)
                        self.copiedsize += f.stat().st_size
                        self.renamedfiles += 1
                        self.copiedfiles += 1
                        pbar.update(f.stat().st_size)
                else:
                    copyfile_by_blocks(srcfile, dstfile)
                    self.copiedsize += f.stat().st_size
                    self.copiedfiles += 1
                    pbar.update(f.stat().st_size)

        return self.copiedfiles


# filecmp.dircmp(SOURCE_PATH,DESTINATION_PATH).report()
copia1 = CopyTask(SOURCE_PATH, DESTINATION_PATH, pbar=True)

print(copia1)
print(r"Número de Ficheros en {} = {}".format(SOURCE_PATH, len(copia1.sourcefiles)))
print("Tamaño total de la carpeta origen: {:.2f}MBs".format(round(copia1.totalsize/1024/1024, 2)))

t = Timer(name="class", logger=None)
t.start()

# copia1.do_copy()
# copia1.do_copy(datetime.strptime("2019/01/01", "%Y/%m/%d"))
# copia1.do_copy(to_date=datetime.strptime("2019/01/01", "%Y/%m/%d"))
copia1.do_copy(datetime.strptime("2019/01/01", "%Y/%m/%d"),
               datetime.strptime("2019/01/31", "%Y/%m/%d"))

elapsed_time = t.stop()

print("Tamaño seleccionado para copiar: {:.2f}MBs".format(round(copia1.selectedsize/1024/1024, 2)))
print("Ficheros con mismo nombre pero distintos (renombrar): {}".format(copia1.renamedfiles))
print("Ficheros idénticos (saltar): {}".format(copia1.skippedfiles))
print("Ficheros copiados: {} (tamaño: {:.2f}MBs)".format(copia1.copiedfiles, round(copia1.copiedsize/1024/1024, 2)))
print("Tiempo transcurrido: {:.4f} segundos".format(round(elapsed_time, 4)))

