import math
from tkinter import *
from unittest import result
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('./imagenes/pulgon-2.jpg')
cv2.imshow("Original",img)
cv2.calcHist([img],[0],None,[256],[0,256])
plt.hist(img.ravel(),256,[0,256])
plt.title('Histograma Orginal')
plt.show()

img_to_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
img_to_yuv[:,:,0] = cv2.equalizeHist(img_to_yuv[:,:,0])
hist_equalization_result = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)

cv2.imshow("Ecualizado",hist_equalization_result)
cv2.calcHist([hist_equalization_result],[0],None,[256],[0,256])
plt.hist(hist_equalization_result.ravel(),256,[0,256])
plt.title('Histograma Ecualizado')
plt.show()

cv2.imwrite('./imagenes/hist_eq.jpg',hist_equalization_result)

cv2.waitKey(0) #Mostrará la ventana infinitamente hasta que se presione cualquier tecla.
cv2.destroyAllWindows()
result.config(text="Deteccion Ecualización realizada") #Permite a los usuarios destruir o cerrar todas las ventanas en cualquier momento después de salir del script.