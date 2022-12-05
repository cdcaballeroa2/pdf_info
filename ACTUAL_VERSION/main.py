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
#initializing.initialize()

# Contenedor de los archivos PDF
MAIN_FOLDER = "C:\DANE_test"

folders_list = [folder.name for folder in os.scandir(MAIN_FOLDER) if folder.is_dir()]

for folder in folders_list:
    print(f"Procesando carpeta {folder}")
    file_preprocessing.process_folder(MAIN_FOLDER, folder)