import os
from time import time
import pdfplumber
from utils import folders
from tqdm import tqdm
from preprocessing import text_preprocessing, image_preprocessing
import numpy as np
import glob


def process_file(filename, folders_list):
    """
      Función principal, que se encarga de procesar los
      archivos PDF ingresados.
    """
    head = os.path.split(filename)[1].replace('.pdf', '')
    folder_output = folders.verify_folder(os.sep.join([folders_list['IMAGE_FOLDER'], head]))
    # Se crea el diccionario que contiene la informacion del archivo
    output = {}
    # f = open(os.sep.join([folders_list['TXT_FOLDER'], head + ".txt"]), "w")
    # Abre el PDF para procesarlo
    archivo = pdfplumber.open(filename)
    # Contador de paginas
    pages = archivo.pages
    output['pags'] = len(pages) #Cantidad de paginas
    output['text'] = [] #Texto del archivo
    output['types'] = [] #Clasificacion de paginas

    # Lee cada pagina del PDF
    for page in tqdm(pages):
        # print(f"\n-----------------PAGINA {k}---------------")
        # Extrae el texto de la pagina
        text_page = page.extract_text()
        # Preprocesa el texto
        text_page = text_preprocessing.validate_content(text_page)
        # photo = text_page[1]
        if (len(text_page[0]) > 0) and (not text_page[0].isspace()):
            # Caso de texto digitalizado
            # Guarda el texto en un diccionario
            output['text'] = output['text'] + [text_page[0]]
            # Guarda la categoria obtenida
            output['types'] = output['types'] + ['DIGITAL']
        else:
            # Caso como imagen
            ## Guarda la imagen
            image_file = os.sep.join([folders_list['IMAGE_FOLDER'], head, f"{k}.jpg"])
            page.to_image(resolution=200).save(image_file, format="JPEG")

            # Procesa la imagen
            ## Verifica tipo de imagen
            t_img = image_preprocessing.image_cat(image_file)
            if t_img == 0:
                output['text'] = output['text'] + [""]
                output['types'] = output['types'] + ['VACIO']
            else:
                to_process = True
                ff = ''
                # Se hace verificacion con alternativa sencilla
                ff = image_preprocessing.image_text(image_file)
                if not text_preprocessing.is_valid_text(ff):
                    ff = image_preprocessing.image_text(image_file, preprocess=True)
                    output['types'] = output['types'] + ['REGULAR']
                else:
                    output['types'] = output['types'] + ['ACEPTABLE']

                output['text'] = output['text'] + [ff]

    return output


def process_folder(folder_person):
    folders_list = folders.initialize_folders(folder_person)
    list_files = glob.glob(os.path.join(folder_person, "*.pdf"))
    output = {}  # Salida de datos

    # Obtencion de archivos de persona
    for fil in list_files:

        # Contador de tiempo para archivo
        time0 = time()

        try:
            # Procesa archivo y obtiene textos
            output[fil] = process_file(fil, folders_list)
            # Incluye tiempos
            time1 = time()
            output[fil]['time'] = round(time1 - time0, 2)
            output[fil]['state'] = "PROCESADO"
        except Exception as ex:
            # Guarda el dato del error en archivo
            output[fil]['error'] = str(ex)
            output[fil]['state'] = "REVISION"

