import cv2
import numpy as np
imagen = cv2.imread('pulgon3.2jpg')

th = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)

#Para versiones OpenCV3:
# img1,contornos1,hierarchy1 = cv2.findContours(th, cv2.RETR_EXTERNAL,
#       cv2.CHAIN_APPROX_NONE)
# img2,contornos2,hierarchy2 = cv2.findContours(th, cv2.RETR_EXTERNAL,
#       cv2.CHAIN_APPROX_SIMPLE)
#Para versiones OpenCV4:
contornos1,hierarchy1 = cv2.findContours(th, cv2.RETR_EXTERNAL,
           cv2.CHAIN_APPROX_NONE)
contornos2,hierarchy2 = cv2.findContours(th, cv2.RETR_EXTERNAL,
           cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imagen, contornos1, -1, (0,255,0), 3)
print ('len(contornos1[2])=',len(contornos1[2]))
print ('len(contornos2[2])=',len(contornos2[2]))
cv2.imshow('imagen',imagen)
cv2.imshow('th',th)
cv2.waitKey(0)
cv2.destroyAllWindows()