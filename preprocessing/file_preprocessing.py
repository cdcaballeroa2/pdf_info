import os
from time import time
import pdfplumber
from utils import folders
from tqdm import tqdm
from preprocessing import text_preprocessing, image_preprocessing


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
    pags = {}
    k = 1
    # Lee cada pagina del PDF
    for page in tqdm(archivo.pages):
        # print(f"\n-----------------PAGINA {k}---------------")
        t0 = time()
        # Extrae el texto de la pagina
        text_page = page.extract_text()
        # Preprocesa el texto
        text_page = text_preprocessing.validate_content(text_page)
        photo = text_page[1]
        if (len(text_page[0]) > 0) and (not text_page[0].isspace()):
            # Caso de texto digitalizado
            # Guarda el texto en un diccionario
            pags[k] = text_page[0]
            # print(text_page[0])
        else:
            # Caso como imagen
            ## Guarda la imagen
            image_file = os.sep.join([folders_list['IMAGE_FOLDER'], head, f"{k}.jpg"])
            page.to_image(resolution=200).save(image_file, format="JPEG")
            # Procesa la imagen
            ## Verifica tipo de imagen

            ## Caso en el que es digitalizado

            ## Caso en el que es un escaneo

            if photo:
                ## Caso en el que es foto
                ff = image_preprocessing.image_text(image_file, preprocess=True)
            else:
                ff = image_preprocessing.image_text(image_file)
            # Verificar si el texto esta en blanco
            if not text_preprocessing.delete_blank_lines(ff):
                raise ValueError(f"Pagina en blanco, #{k}")
            # Guarda el dato en el diccionario
            pags[k] = ff

        # Registro de tiempo
        t2 = time()
        # print(f"\nTiempo: {t2-t0} ")

        # Guarda la linea en el TXT
        f.write(f"\n----------------PAGINA {k}---------------\n")
        f.write(pags[k])
        k = k + 1
    f.close()
    return len(archivo.pages)
