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

def get_bounds(img0, offset=20, little_dif=False):
    """
    Obtiene los bordes de una imagen con fondo blanco
    :param img0:
    :param offset:
    :param little_dif:
    :return:
    """
    border = 10
    img0 = cv.copyMakeBorder(img0, border, border, border, border, cv.BORDER_CONSTANT, value=[255, 255, 255])
    bn_img = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)

    t, dst = cv2.threshold(bn_img, 254, 255, cv2.THRESH_BINARY)  # np.maximum(dst1,dst2)
    t, dst = cv2.threshold(dst, 254, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    invalid = True
    revision = False
    maxa = 0
    for c in contours:
        area = cv2.contourArea(c)
        Pa = area / (dst.shape[0] * dst.shape[1])

        if 0.99 > Pa > 0.3:
            (x, y, w, h) = cv2.boundingRect(c)
            roi = img0[y:y + h, x:x + w]
            Pa = area / (dst.shape[0] * dst.shape[1])
            Fa = h * w / (dst.shape[0] * dst.shape[1])
            if (0.95 > Fa > 0.4 and (h - 20) * (w - 20) / (img0.shape[0] * img0.shape[1]) < 0.98) or little_dif:
                invalid = False
                revision = False
                break
            elif Fa <= 0.40:
                revision = True
        elif Pa > 0.1:
            (x, y, w, h) = cv2.boundingRect(c)
            roi = img0[y:y + h, x:x + w]
            Fa = h * w / (dst.shape[0] * dst.shape[1])
            if Fa < 0.3:
                revision = True

    if invalid:
        return revision, img0
    else:
        return revision, roi

def isgray(img):
    """
    Verifica si una imagen esta en grises o RGB.
    :param img:
    :return:
    """
    if len(img.shape) < 3: return True
    if img.shape[2]  == 1: return True
    b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
    if (b==g).all() and (b==r).all(): return True
    return False

def image_cat(imgFile):
  """
  Obtiene la categoria de una imagen.
  Input: Ruta de ubicacion de la imagen (string)
  """
  output_type = 0
  offset = 1

  img = cv.imread(imgFile)

  ##Verificacion
  bn_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  #Oscuros
  p_dark = sum(sum(bn_img<15))*100/(bn_img.shape[0]*bn_img.shape[1])
  #Blancos
  p_white = sum(sum(bn_img==255))*100/(bn_img.shape[0]*bn_img.shape[1])
  #Claros
  p_clear = sum(sum(bn_img>250))*100/(bn_img.shape[0]*bn_img.shape[1])

  #print('Gris' if isgray(img) else 'RGB')
  if p_white > 99:
    output = "Blanco"
  else:
    if (p_white>70 and p_dark>0.7) or p_white>83 or (p_clear>80 and p_clear-p_white>5) or (p_clear-p_white>15 and p_dark>0.7):
      output = "Calidad optima\n" + f"Blancos {round(p_white)}, Claros {round(p_clear)}, Oscuros {round(p_dark,2)}"
      output_type = 1
    else:
      if p_clear > 70 and p_clear-p_white>1:
        output = "Calidad media / Escaneo\n" + f"Blancos {round(p_white)}, Claros {round(p_clear)}, Oscuros {round(p_dark,2)}"
        output_type = 2
      else:
        output = "Calidad baja / Foto\n" + f"Blancos {round(p_white)}, Claros {round(p_clear)}, Oscuros {round(p_dark,2)}"
        little_dif = (p_clear-p_white)<=2
        if p_white>1:
          revision, imgf = get_bounds(img,offset, little_dif)
          if revision:
            output_type = 4
          else:
            output_type = 3
        else:
          output_type = 3

  return output_type