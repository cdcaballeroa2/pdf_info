import cv2 as cv
import pytesseract
import cv2

def image_text(imgFile, ncuadro=23, par_c=5, preprocess=False):
    """
    Obtiene texto de una imagen binarizada y sin binarizar
    Input: Ruta de ubicacion de la imagen (string)
    """
    #print(f"----------Imagen: {imgFile}")
    img = cv.imread(imgFile)

    if preprocess:
        ad_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        th2 = cv.adaptiveThreshold(ad_img, 255, cv.ADAPTIVE_THRESH_MEAN_C, \
                                   cv.THRESH_BINARY, ncuadro, par_c)
        txt2 = pytesseract.image_to_string(th2)  # , lang="spa")
        return txt2
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        txt1 = pytesseract.image_to_string(img)  # , lang="spa")
        return txt1

