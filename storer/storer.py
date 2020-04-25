import filecmp
from os import scandir
from os.path import isfile, join, getsize
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


# filecmp.dircmp(SOURCE_PATH,DESTINATION_PATH).report()

sourcefiles = [f for f in scandir(SOURCE_PATH) if f.is_file()]   # https://www.python.org/dev/peps/pep-0471/  @scandir

print(r"Número de Ficheros en " + SOURCE_PATH + " = " + str(len(sourcefiles)))
totalsize = sum(f.stat().st_size for f in sourcefiles if f.is_file())
print("Tamaño total: {:.2f}MBs".format(round(totalsize/1024/1024, 2)))

skippedfiles = 0
renamedfiles = 0
copiedfiles = 0
copiedsize = 0
deltafiles = 0

print("Copiando...")
t = Timer(name="class", logger=None)
t.start()

for f in sourcefiles:
    srcfile = f.path
    dstfile = join(DESTINATION_PATH, f.name)
    if isfile(dstfile):
        if is_the_same_file(srcfile, dstfile):
            skippedfiles += 1
        else:
            dstfile = rename_file(dstfile)
            copyfile_by_blocks(srcfile, dstfile)
            copiedsize += f.stat().st_size
            renamedfiles += 1
            copiedfiles += 1
    else:
        copyfile_by_blocks(srcfile, dstfile)
        copiedsize += f.stat().st_size
        copiedfiles += 1

elapsed_time = t.stop()
print("Ficheros con mismo nombre pero distintos (renombrar): %d " % renamedfiles)
print("Ficheros idénticos (saltar): %d" % skippedfiles)
print("%d copiados. Tamaño copiado: {:.2f}MBs".format(round(copiedsize/1024/1024, 2)) % copiedfiles)
print("Tiempo transcurrido: {:.4f} segundos".format(round(elapsed_time, 4)))

