import cv2
import numpy as np
from matplotlib import pyplot as plt
 
img = cv2.imread('./imagenes/pulgon-2.jpg_sobel.jpg')
 
#Crea el kernel
kernel3x3 = np.ones((3,3),np.float32)/9.0
kernel5x5 = np.ones((5,5),np.float32)/25.0

#Filtra la imagen utilizando el kernel anterior
salida3 = cv2.filter2D(img,-1,kernel3x3)
salida5 = cv2.filter2D(img,-1,kernel5x5)

cv2.imshow("original",img)
cv2.imshow("salida3",salida3)
cv2.imshow("salida5",salida5)

cv2.waitKey(0)