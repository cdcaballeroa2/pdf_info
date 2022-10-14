import glob
import os
import shutil
from time import time
from preprocessing import file_preprocessing, plot_performance
from utils import folders, initializing

# Ejecutar en Terminal la siguiente línea ANTES de ejecutar por primera vez:
# sudo chmod 777 /etc/ImageMagick-6/policy.xml

# Actualizar opciones de seguridad
initializing.initialize()

# Contenedor de los archivos PDF
MAIN_FOLDER = '/home/david/Documents/pdf_process'

folders_list = folders.initialize_folders(MAIN_FOLDER)

list_files = glob.glob(os.path.join(MAIN_FOLDER, "*.pdf"))
time_list = []
npage_list = []
error_cant = 0
counter = 0

for fil in list_files:
    counter = counter + 1
    time0 = time()
    print(f"\nArchivo {fil}, {len(npage_list) + 1}/{len(list_files)}\n")
    try:
        npags = file_preprocessing.process_file(fil, folders_list)
        npage_list.append(npags)
        time1 = time()
        time_list.append(round(time1 - time0, 2))
        state = "PDF_PROCESSED"
    except Exception as ex:
        print('ERROR ' + str(ex))
        error_cant += 1
        f = open("/home/david/Documents/results_pdf/errors.txt", "a")
        f.write("-" + fil + ":\n" + str(ex) + '\n')
        f.close()
        state = "PDF_ERRORS"
    finally:
        err_cants = [error_cant, counter - error_cant]
        if len(time_list)>0:
            plot_performance.plots(time_list, npage_list, err_cants)
        f_out = os.sep.join([folders_list[state],
                             os.path.split(fil)[1]]
                            )
        shutil.move(fil, f_out)

print("Tiempo ejecución\n")
print(f"{len(npage_list)}\t archivos.")
print(f"Tiempo: {round(sum(time_list), 2)}\t segundos.")
print(f"Tiempo/archivo: {round(sum(time_list) / len(npage_list), 4)}\t segundos.")
