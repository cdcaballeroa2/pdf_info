import glob
import os
from time import time
from preprocessing import file_preprocessing
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
# counter = 1
# time0 = time()
for fil in list_files[0:3]:
    time0 = time()
    print(f"\nArchivo {fil}, {len(npage_list) + 1}/{len(list_files)}\n")
    npags = file_preprocessing.process_file(fil, folders_list)
    npage_list.append(npags)
    # counter = counter + 1
    time1 = time()
    time_list.append(round(time1 - time0, 2))
# time1 = time()
print("Tiempo ejecución\n")
print(f"{len(npage_list)}\t archivos.")
print(f"Tiempo: {round(sum(time_list), 2)}\t segundos.")
print(f"Tiempo/archivo: {round(sum(time_list) / len(npage_list), 2)}\t segundos.")
