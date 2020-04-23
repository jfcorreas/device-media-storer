import filecmp
from os import listdir
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


sourcefiles = [f for f in listdir(SOURCE_PATH)
               if isfile(join(SOURCE_PATH, f))]
print(r"Número de Ficheros en " + SOURCE_PATH + " = " + str(len(sourcefiles)))

print("Copiando...")

skipped = 0
renamed = 0
copiedfiles = 0
totalsize = 0
t = Timer(name="class", logger=None)
t.start()
for f in sourcefiles:
    srcfile = join(SOURCE_PATH, f)
    dstfile = join(DESTINATION_PATH, f)
    totalsize += getsize(srcfile)
    if isfile(dstfile):
        if is_the_same_file(srcfile, dstfile):
            skipped += 1
        else:
            dstfile = rename_file(dstfile)
            copyfile_by_blocks(srcfile, dstfile)
            renamed += 1
    else:
        copyfile_by_blocks(srcfile, dstfile)
        copiedfiles += 1
elapsed_time = t.stop()

print(str(copiedfiles) + " copiados. Tamaño total: {:.2f}".format(round(totalsize/1024/1024, 2)) + "MBs")
print("Tiempo transcurrido: {:.4f}".format(round(elapsed_time, 4)) + " segundos")
print("Ficheros idénticos (saltar): " + str(skipped))
print("Ficheros para renombrar: " + str(renamed))


