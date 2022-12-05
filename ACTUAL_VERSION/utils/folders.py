import os
import unicodedata
import re


def initialize_folders(root_folder):
    """
    Inicializa las carpetas de uso.
    :param root_folder:
    :return:
    """
    folders = [
        'IMAGE_FOLDER',
        'TXT_FOLDER'
    ]

    pr_folder = {}

    for folder in folders:
        str_folder = os.sep.join([root_folder, folder])
        pr_folder[folder] = str_folder
        verify_folder(str_folder)

    return pr_folder


def verify_folder(dir_folder):
    "Crea una carpeta para guardar las imagenes obtenidas"
    if not os.path.exists(dir_folder):
        os.mkdir(dir_folder)
    return dir_folder


def normalized_path(cadena):
    """
        Normaliza el nombre de una carpeta, antes de crearse.
        :param cadena:
        :return:
    """
    s = ''.join((c for c in unicodedata.normalize('NFD', cadena) if unicodedata.category(c) != 'Mn'))
    s = re.sub(r"[^a-zA-Z0-9]", "", s)
    return s
