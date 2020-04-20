from os import listdir
from os.path import isfile, join, getsize
from codetiming import Timer                # https://github.com/realpython/codetiming

SOURCE_PATH = "../source_files"
DESTINATION_PATH = "../dest_files"


def copyfiles(src, dst):
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            fdst.write(fsrc.read())

            # for x in iter(lambda: fsrc.read(16384), ""):
            #    fdst.write(x)


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
    copyfiles(srcpath, dstpath)
    copiedfiles += 1
elapsed_time = t.stop()

print(str(copiedfiles) + " copiados. Tamaño total: {:.2f}".format(round(totalsize/1024/1024, 2)) + "MBs")
print("Tiempo transcurrido: {:.4f}".format(round(elapsed_time, 4)) + " segundos")
print("Ficheros sobrescritos: " + str(overwrited))