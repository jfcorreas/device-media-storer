from os import listdir
from os.path import isfile, join, getsize
from codetiming import Timer                # https://github.com/realpython/codetiming

SOURCE_PATH = "/home/jfcm02/Proyectos/Desarrollo/TestData/source_files"
SOURCE_LARGEFILES_PATH = "/home/jfcm02/Proyectos/Desarrollo/TestData/source_files_large"
DESTINATION_PATH = "/home/jfcm02/Proyectos/Desarrollo/TestData/dest_files"


def copyfile(src, dst):
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            fdst.write(fsrc.read())


def copyfile_16kblock(src, dst):
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            for x in iter(lambda: fsrc.read(16384), ""):
                if not x:
                    break
                fdst.write(x)


sourcefiles = [f for f in listdir(SOURCE_PATH)
               if isfile(join(SOURCE_PATH, f))]
print(r"Número de Ficheros en " + SOURCE_PATH + " = " + str(len(sourcefiles)))

print("Copiando...")

overwrited = 0
copiedfiles = 0
totalsize = 0
t = Timer(name="class", logger=None)
t.start()
for f in sourcefiles:
    srcpath = join(SOURCE_PATH, f)
    dstpath = join(DESTINATION_PATH, f)
    totalsize += getsize(srcpath)
    if isfile(dstpath):
        overwrited += 1
    copyfile(srcpath, dstpath)
    copiedfiles += 1
elapsed_time = t.stop()

print(str(copiedfiles) + " copiados. Tamaño total: {:.2f}".format(round(totalsize/1024/1024, 2)) + "MBs")
print("Tiempo transcurrido: {:.4f}".format(round(elapsed_time, 4)) + " segundos")
print("Ficheros sobrescritos: " + str(overwrited))

sourcefiles = [f for f in listdir(SOURCE_LARGEFILES_PATH)
               if isfile(join(SOURCE_LARGEFILES_PATH, f))]
print(r"Número de Ficheros en " + SOURCE_LARGEFILES_PATH + " = " + str(len(sourcefiles)))

print("Copiando...")

overwrited = 0
copiedfiles = 0
totalsize = 0
t = Timer(name="class", logger=None)
t.start()
for f in sourcefiles:
    srcpath = join(SOURCE_LARGEFILES_PATH, f)
    dstpath = join(DESTINATION_PATH, f)
    totalsize += getsize(srcpath)
    if isfile(dstpath):
        overwrited += 1
    copyfile_16kblock(srcpath, dstpath)
    copiedfiles += 1
elapsed_time = t.stop()

print(str(copiedfiles) + " copiados. Tamaño total: {:.2f}".format(round(totalsize/1024/1024, 2)) + "MBs")
print("Tiempo transcurrido: {:.4f}".format(round(elapsed_time, 4)) + " segundos")
print("Ficheros sobrescritos: " + str(overwrited))