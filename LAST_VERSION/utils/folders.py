import os


def initialize_folders(root_folder):
    """
    Inicializa las carpetas de uso.
    :param root_folder:
    :return:
    """
    folders = [
        'IMAGE_FOLDER',
        'TXT_FOLDER',
        'PDF_PROCESSED',
        'PDF_ERRORS',
        'PDF_REVISION'
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

