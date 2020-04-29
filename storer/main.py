from storer.fileops.filecopier import CopyTask

from codetiming import Timer                # https://github.com/realpython/codetiming
from datetime import datetime, timedelta

SOURCE_PATH = "/home/jfcm02/Proyectos/Desarrollo/TestData/source_files"
DESTINATION_PATH = "/home/jfcm02/Proyectos/Desarrollo/TestData/dest_files"

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

print("Ficheros seleccionados para copiar: {} ({:.2f}MBs)".format(len(copia1.selectedfiles), round(copia1.selectedsize/1024/1024, 2)))
print("Ficheros con mismo nombre pero distintos (renombrar): {}".format(copia1.renamedfiles))
print("Ficheros idénticos (saltar): {}".format(copia1.skippedfiles))
print("Ficheros copiados: {} (tamaño: {:.2f}MBs)".format(copia1.copiedfiles, round(copia1.copiedsize/1024/1024, 2)))
print("Tiempo transcurrido: {:.4f} segundos".format(round(elapsed_time, 4)))