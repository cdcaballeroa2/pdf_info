import glob
import os
import shutil
from time import time
from preprocessing import file_preprocessing, plot_performance
from utils import folders, initializing
import numpy as np

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
cat_totals = np.zeros(6)

for fil in list_files:
    counter = counter + 1
    time0 = time()
    print(f"\nArchivo {fil}, {len(npage_list) + 1}/{len(list_files)}\n")
    try:
        #Procesa archivo
        cat_doc, revision_pages, pags_text = file_preprocessing.process_file(fil, folders_list)
        # Incluye la cantidad de paginas
        npage_list.append(np.sum(cat_doc))
        # Incluye tiempos
        time1 = time()
        time_list.append(round(time1 - time0, 2))
        # Incluye las cantidades por categoria
        cat_totals = cat_totals + cat_doc
        # Asigna la carpeta segun la tipologia
        if len(revision_pages) > 0:
            state = "PDF_REVISION"
            # Guarda el dato de revision en archivo
            error_cant += 1
            f = open("/home/david/Documents/results_pdf/revision.txt", "a")
            f.write("-" + fil + ":\tPaginas:" + str(revision_pages) + '\n')
            f.close()
        else:
            state = "PDF_PROCESSED"
    except Exception as ex:
        # Guarda el dato del error en archivo
        error_cant += 1
        f = open("/home/david/Documents/results_pdf/errors.txt", "a")
        f.write("-" + fil + ":\t" + str(ex) + '\n')
        f.close()
        # Asigna la carpeta segun la tipologia
        state = "PDF_ERRORS"
    finally:
        #Obtiene graficas de rendimiento
        err_cants = [error_cant, counter - error_cant]
        if len(time_list)>0:
            plot_performance.resume_time(time_list, npage_list, err_cants)
            plot_performance.resume_quality(cat_totals,npage_list)
        #Guarda el PDF donde fue asignado
        f_out = os.sep.join([folders_list[state],
                             os.path.split(fil)[1]]
                            )
        shutil.move(fil, f_out)

print("Tiempo ejecución\n")
print(f"{len(npage_list)}\t archivos.")
print(f"Tiempo: {round(sum(time_list), 2)}\t segundos.")
print(f"Tiempo/archivo: {round(sum(time_list) / len(npage_list), 4)}\t segundos.")
