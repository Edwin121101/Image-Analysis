import cv2
img = cv2.imread('./imagenes/pulgon3.1.jpg', cv2.IMREAD_GRAYSCALE)

_, binary_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)


cv2.imshow("Imagen Binarizada", binary_img)

cv2.imwrite("./imagenes/binarizado.jpg", binary_img)



cv2.waitKey(0)
cv2.destroyAllWindows()
