import os
from time import time
import pdfplumber
from utils import folders
from tqdm import tqdm
from preprocessing import text_preprocessing, image_preprocessing
import numpy as np


def process_file(filename, folders_list):
    """
      Función principal, que se encarga de procesar los
      archivos PDF ingresados.
    """
    head = os.path.split(filename)[1].replace('.pdf', '')
    folder_output = folders.verify_folder(os.sep.join([folders_list['IMAGE_FOLDER'], head]))
    # Se crea el TXT para incluir lineas de texto
    f = open(os.sep.join([folders_list['TXT_FOLDER'], head + ".txt"]), "w")
    # Abre el PDF para procesarlo
    archivo = pdfplumber.open(filename)
    # Obtencion de texto total
    pags_text = {}
    # Contador de paginas
    k = 1
    # Contador de clasificacion
    cat_doc = np.zeros(6)
    revision_pages = []
    # Lee cada pagina del PDF
    for page in tqdm(archivo.pages):
        # print(f"\n-----------------PAGINA {k}---------------")
        # Extrae el texto de la pagina
        text_page = page.extract_text()
        # Preprocesa el texto
        text_page = text_preprocessing.validate_content(text_page)
        #photo = text_page[1]
        if (len(text_page[0]) > 0) and (not text_page[0].isspace()):
            # Caso de texto digitalizado
            # Guarda el texto en un diccionario
            pags[k] = text_page[0]
            # Guarda la categoria obtenida
            cat_doc[5] += 1
        else:
            # Caso como imagen
            ## Guarda la imagen
            image_file = os.sep.join([folders_list['IMAGE_FOLDER'], head, f"{k}.jpg"])
            page.to_image(resolution=200).save(image_file, format="JPEG")

            # Procesa la imagen
            ## Verifica tipo de imagen
            t_img = image_preprocessing.image_cat(image_file)
            to_process = True
            while to_process and t_img!=0:
                if t_img==1:
                    ## Caso en el que es digitalizado
                    ff = image_preprocessing.image_text(image_file)
                elif t_img==2:
                    ## Caso en el que es un escaneo
                    ## TODO falta el preprocess
                    ff = image_preprocessing.image_text(image_file)
                elif t_img==3:
                    ## Caso en el que es foto
                    ff = image_preprocessing.image_text(image_file, preprocess=True)
                elif t_img==4:
                    ## Caso que pasa a revisión
                    ff = ''
                    revision_pages.append(k)
                    to_process = False
                    break
                # Verificar si el texto sigue en blanco
                if not text_preprocessing.is_valid_text(ff):
                    t_img += 1
                else:
                    to_process = False
                    break

            #Guarda la categoria obtenida
            cat_doc[t_img] += 1

            # Guarda el texto en el diccionario
            pags[k] = ff

        # Guarda la linea en el TXT
        f.write(f"\n----------------PAGINA {k}---------------\n")
        f.write(pags[k])
        k = k + 1
    f.close()
    return cat_doc, revision_pages, pags_text
