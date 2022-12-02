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

folders_list = [folder.name for folder in os.scandir(MAIN_FOLDER) if folder.is_dir()]

for folder in folders_list:
    file_preprocessing.process_folder(MAIN_FOLDER,folder)

print("Tiempo ejecución\n")
print(f"{len(npage_list)}\t archivos.")
print(f"Tiempo: {round(sum(time_list), 2)}\t segundos.")
print(f"Tiempo/archivo: {round(sum(time_list) / len(npage_list), 4)}\t segundos.")