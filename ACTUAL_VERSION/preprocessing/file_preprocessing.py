import datetime
import os
from time import time
import pdfplumber
from ACTUAL_VERSION.utils import folders
from tqdm import tqdm
from ACTUAL_VERSION.preprocessing import text_preprocessing, image_preprocessing
from ACTUAL_VERSION.processing import date_processing
import numpy as np
import glob

import pprint


def process_file(filename, folders_list):
    """
      Función principal, que se encarga de procesar los
      archivos PDF ingresados.
    """
    head = folders.normalized_path(str(os.path.split(filename)[1].replace('.pdf', '')))
    folder_output = folders.verify_folder(os.sep.join([folders_list['IMAGE_FOLDER'], head]))
    # Se crea el diccionario que contiene la informacion del archivo
    output = {}
    # f = open(os.sep.join([folders_list['TXT_FOLDER'], head + ".txt"]), "w")
    # Abre el PDF para procesarlo
    archivo = pdfplumber.open(filename)
    # Contador de paginas
    pages = archivo.pages
    output['pags'] = len(pages)  # Cantidad de paginas
    output['text'] = []  # Texto del archivo
    output['types'] = []  # Clasificacion de paginas
    # Contador de paginas
    k = 1

    # Lee cada pagina del PDF
    for page in pages:
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
                # Se hace verificacion con alternativa sencilla
                ff = image_preprocessing.image_text(image_file)
                if not text_preprocessing.is_valid_text(ff):
                    ff = image_preprocessing.image_text(image_file, preprocess=True)
                    output['types'] = output['types'] + ['REGULAR']
                else:
                    output['types'] = output['types'] + ['ACEPTABLE']

                output['text'] = output['text'] + [ff]

    return output


def process_folder(main_folder, subfolder, save_text: bool = False):
    folder_person = os.path.join(main_folder, subfolder)
    folders_list = folders.initialize_folders(folder_person)
    list_files = glob.glob(os.path.join(folder_person, "*.pdf"))
    output = {}  # Salida de datos
    # Rangos de fechas trabajadas
    date_lst = {}
    # Contador de rangos de fechas
    date_counter = 0
    # Bandera de estado de archivos
    valid = True
    # Obtencion de archivos de persona
    for fil in tqdm(list_files):
        fil_key = os.path.split(os.path.splitext(fil)[0])[1]
        # Contador de tiempo para archivo
        time0 = time()

        try:
            # Procesa archivo y obtiene textos
            output[fil_key] = process_file(fil, folders_list)
            # Incluye tiempos
            time1 = time()
            output[fil_key]['time'] = round(time1 - time0, 2)

            # Realiza obtencion de fechas

            output[fil_key]['experience_data'] = date_processing.get_dates_from_txt(
                str_data=" ".join(output[fil_key]['text'])
            )

            if output[fil_key]['experience_data']['experience'] == 0:
                output[fil_key]['state'] = "REVISION"
                output[fil_key]['error'] = {'type': 'FECHA',
                                            'description': "No hay rangos de fecha"}
                valid = False
            else:
                for el in list(output[fil_key]['experience_data']['dates'].keys()):
                    date_lst[date_counter] = {'dates': output[fil_key]['experience_data']['dates'][el]['dates'],
                                              'file': fil}
                    date_counter += 1
                output[fil_key]['state'] = "PROCESADO"

        except Exception as ex:
            # Guarda el dato del error en archivo
            output[fil_key]['error'] = {'type': 'FECHA',
                                        'description': str(ex)}
            output[fil_key]['state'] = "REVISION"
            valid = False
        finally:
            if not save_text:
                output[fil_key]['text'] = ""

        final_output = {'total_experience': date_processing.get_dates_from_person(date_lst) if date_counter > 0 else 0,
                        'files': output,
                        'last_revision': datetime.datetime.now(),
                        'revision_status': valid}

    pprint.pprint(final_output)

    return final_output
