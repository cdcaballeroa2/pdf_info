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
        # photo = text_page[1]
        if (len(text_page[0]) > 0) and (not text_page[0].isspace()):
            # Caso de texto digitalizado
            # Guarda el texto en un diccionario
            pags_text[k] = text_page[0]
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
            ff = ''
            while to_process and t_img != 0:
                if t_img == 1:
                    ## Caso en el que es digitalizado
                    ff = image_preprocessing.image_text(image_file)
                elif t_img == 2:
                    ## Caso en el que es un escaneo
                    ## TODO falta el preprocess
                    ff = image_preprocessing.image_text(image_file)
                elif t_img == 3:
                    ## Caso en el que es foto
                    ff = image_preprocessing.image_text(image_file, preprocess=True)
                elif t_img == 4:
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

            # Guarda la categoria obtenida
            cat_doc[t_img] += 1

            # Guarda el texto en el diccionario
            pags_text[k] = ff

        # Guarda la linea en el TXT
        f.write(f"\n----------------PAGINA {k}---------------\n")
        f.write(pags_text[k])
        k = k + 1
    f.close()
    return cat_doc, revision_pages, pags_text


def process_folder(folder_person):
    folders_list = folders.initialize_folders(folder_person)
    list_files = glob.glob(os.path.join(folder_person, "*.pdf"))
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
            # Procesa archivo
            cat_doc, revision_pages, pags_text = process_file(fil, folders_list)
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
            # Obtiene graficas de rendimiento
            err_cants = [error_cant, counter - error_cant]
            if len(time_list) > 0:
                plot_performance.resume_time(time_list, npage_list, err_cants)
                plot_performance.resume_quality(cat_totals, npage_list)
            # Guarda el PDF donde fue asignado
            f_out = os.sep.join([folders_list[state],
                                 os.path.split(fil)[1]]
                                )
            shutil.move(fil, f_out)
