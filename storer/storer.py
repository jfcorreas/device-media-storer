import filecmp
from os import listdir
from os.path import isfile, join, getsize
from codetiming import Timer                # https://github.com/realpython/codetiming

SOURCE_PATH = "/home/jfcm02/Proyectos/Desarrollo/TestData/source_files"
DESTINATION_PATH = "/home/jfcm02/Proyectos/Desarrollo/TestData/dest_files"


def copyfile_by_blocks(src, dst, block=16384):
    """
    Copies a file from source to destination

    :param src: source file
    :param dst: destination file
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
    Verify if two files are the same file

    :param f1: file 1 for comparison
    :param f2: file 2 for comparison
    :return: True if the file src and the file dst are the same file (content and stats). If not return False
    """
    return filecmp.cmp(f1, f2, False) & filecmp.cmp(f1, f2, True)


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
            renamed += 1
    copyfile_by_blocks(srcfile, dstfile)
    copiedfiles += 1
elapsed_time = t.stop()

print(str(copiedfiles) + " copiados. Tamaño total: {:.2f}".format(round(totalsize/1024/1024, 2)) + "MBs")
print("Tiempo transcurrido: {:.4f}".format(round(elapsed_time, 4)) + " segundos")
print("Ficheros idénticos (saltar): " + str(skipped))
print("Ficheros para renombrar: " + str(renamed))


