from tkinter import * #Libreria tkinter para la interfaz
import tkinter as tki
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import imutils
import cv2
from cv2 import bitwise_or           #Libreria OpenCV para el procesamiento de imagenes
import numpy as np   #Libreria numpy para cálculo y análisis de datos (matrices, arreglos)
from matplotlib import pyplot as plt
import math          #Modulo math proporciona funciones que son útiles en teoría de números
from unittest import result
from matplotlib import pyplot as plt #matplotlib es para crear visualizaciones (como el histograma)

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def grises(img):
    imagen = img
    # Agregue este para reajustar el tamaño
    #resized = ResizeWithAspectRatio(imagen, width=300) 
    
    img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Gris', img_gris)
    img_convertida = cv2.cvtColor(img_gris, cv2.COLOR_GRAY2RGB)
    cv2.imshow('Gris convertida', img_convertida)
    
    #concat_grises = cv2.hconcat([resized, img_convertida])
    #cv2.imshow('Resultado Final', concat_grises)

    filenameGris = file+"_gris.jpg"                
    cv2.imwrite(filenameGris, img_convertida)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    result.config(text="Grises Realizada")

def binarizacion(img):
    imagen = img
    img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    #_, binary_img = cv2.threshold(img_gris, 127, 255, cv2.THRESH_BINARY)
    _, binary_img = cv2.threshold(img_gris, 170, 255, cv2.THRESH_BINARY)
    
    cv2.imshow("Imagen Binarizada", binary_img)

    filenameBinarizada = file+"_binarizada.jpg"                
    cv2.imwrite(filenameBinarizada, binary_img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    result.config(text="Binarización Realizada")

def canales(img):
    bgr = img
    cv2.imshow("Original Image", bgr)
    #Muestra la intensidad de los 3 canales
    black = np.zeros(bgr.shape[:2], dtype='uint8')
    b, g, r = cv2.split(bgr)
    blue = cv2.merge([b, black, black])
    green = cv2.merge([black,g,black])
    red = cv2.merge([black, black, r])
    cv2.imshow('Blue', blue)
    cv2.imshow('Green', green)
    cv2.imshow('Red', red)

    filenameBlue = file+"_blue.jpg"                
    cv2.imwrite(filenameBlue, blue)

    filenameGreen = file+"_green.jpg"                
    cv2.imwrite(filenameGreen, green)

    filenameRed = file+"_red.jpg"                
    cv2.imwrite(filenameRed, red)

    #BGR en grises
    # C1 = bgr[:,:,0]
    # C2 = bgr[:,:,1]
    # C3 = bgr[:,:,2]
    # cv2.imshow('B',np.hstack([C1]))
    # cv2.imshow('G',np.hstack([C2]))
    # cv2.imshow('R',np.hstack([C3]))
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    result.config(text="Canales BGR realizado")

#Negativo de imagen
def negativoImagen(img):
    image = img
    inverted_image = np.invert(image)
    cv2.imwrite("./imagenes/img_invertida.jpg", inverted_image)
    cv2.imshow("Original Image",image)
    cv2.imshow("Inverted Image",inverted_image)
    
    plt.figure('Histograma Inverso')
    plt.hist(inverted_image.ravel(), 256, [0, 256])
    plt.title('Histograma Invertido')
    plt.show()

    filenameInvert = file+"_negativo.jpg"                
    cv2.imwrite(filenameInvert, inverted_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    result.config(text="Negativo Realizado") #Permite a los usuarios destruir o cerrar todas las ventanas en cualquier momento después de salir del script.

#Funcion para la ecualización hiperbolica
def ecualizacion(img):
    print("Ecualización Hiperbolica")

    cv2.imshow("Original",img)
    cv2.calcHist([img],[0],None,[256],[0,256])
    plt.hist(img.ravel(),256,[0,256])
    plt.title('Histograma Orginal')
    plt.show()

    img_to_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
    img_to_yuv[:,:,0] = cv2.equalizeHist(img_to_yuv[:,:,0])
    hist_ecualizacion = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)

    cv2.imshow("Ecualizado",hist_ecualizacion)
    cv2.calcHist([hist_ecualizacion],[0],None,[256],[0,256])
    plt.hist(hist_ecualizacion.ravel(),256,[0,256])
    plt.title('Histograma Ecualizado')
    plt.show()

    filenameEq = file+"_ecualizacionHiper.jpg"                
    cv2.imwrite(filenameEq, hist_ecualizacion) #Se guarda la imagen obtenida con extensión ´jpg´ y el nombre de la técnica aplicada

    cv2.waitKey(0) #Mostrará la ventana infinitamente hasta que se presione cualquier tecla.
    cv2.destroyAllWindows()
    result.config(text="Ecualización Hiperbolica Realizada") 


#Función Filtro Promedio
def promedio(img):
    print("Filtro Promedio")

    cv2.imshow("original",img)
    cv2.calcHist([img],[0],None,[256],[0,256])
    plt.hist(img.ravel(),256,[0,256])
    plt.title('Histograma Orginal')
    plt.show()

    #Crea el kernel
    kernel3x3 = np.ones((3,3),np.float32)/9.0
    kernel5x5 = np.ones((5,5),np.float32)/25.0

    #Filtra la imagen utilizando el kernel anterior
    salida3 = cv2.filter2D(img,-1,kernel3x3)
    salida5 = cv2.filter2D(img,-1,kernel5x5)

    cv2.imshow("salida3",salida3)
    cv2.calcHist([salida3],[0],None,[256],[0,256])
    plt.hist(img.ravel(),256,[0,256])
    plt.title('Histograma Kernel 3x3')
    plt.show()

    cv2.imshow("salida5",salida5)
    cv2.calcHist([salida5],[0],None,[256],[0,256])
    plt.hist(img.ravel(),256,[0,256])
    plt.title('Histograma Kernel 5x5')
    plt.show()

    filename3x3 = file+"_kernel3x3.jpg"                
    cv2.imwrite(filename3x3, salida3) #Se guarda la imagen obtenida con extensión ´jpg´ y el nombre de la técnica aplicada

    filename5x5 = file+"_kernel5x5.jpg"                
    cv2.imwrite(filename5x5, salida5) #Se guarda la imagen obtenida con extensión ´jpg´ y el nombre de la técnica aplicada

    cv2.waitKey(0) #Mostrará la ventana infinitamente hasta que se presione cualquier tecla.
    cv2.destroyAllWindows()
    result.config(text="Filtro Promedio Realizado") 


#Funcion que realiza la deteccion de bordes de sobel
def sobel(img): #TODO: create a formula to get an "automatic" way to apply displacement 
    print("Sobel")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Tomamos nuestra imagen a escala de grises

    cv2.imshow('Entrada', image) #Muestra la imagen de entrada
    cv2.calcHist([image],[0],None,[256],[0,256]) #Se calcula el histograma de la imagen de entrada
    #ravel se usa para cambiar una matriz bidimensional o una matriz multidimensional en una matriz aplanada contigua
    plt.hist(image.ravel(),256,[0,256])            
    plt.title('Histograma de entrada') #Titulo del histograma de la imagen de entrada
    plt.show() #Muestra el histograma de la imagen de entrada

    x = cv2.Sobel(gray,cv2.CV_16S,1,0)
    y = cv2.Sobel(gray,cv2.CV_16S,0,1)
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    sobel = cv2.addWeighted(absX,0.5,absY,0.5,0)

    cv2.imshow('Sobel', sobel) #Muestra la imagen despues de la funcion Sobel
    cv2.calcHist([sobel],[0],None,[256],[0,256]) #Calcula el histograma de la imagen de salida
    plt.hist(sobel.ravel(),256,[0,256])
    plt.title('Histograma Sobel') #Titulo del histograma de la imagen de salida
    plt.show() #Muestra el histograma de la imagen de salida

    filename = file+"_sobel.jpg"                
    cv2.imwrite(filename, sobel) #Se guarda la imagen obtenida con extensión ´jpg´ y el nombre de la técnica aplicada

    cv2.waitKey(0) #Mostrará la ventana infinitamente hasta que se presione cualquier tecla.
    cv2.destroyAllWindows()
    result.config(text="Operador Sobel Realizada") #Permite a los usuarios destruir o cerrar todas las ventanas en cualquier momento después de salir del script.

#Segmentar imagen
def deteccionBordes(img):
    imagen = img
    
    gauss = cv2.GaussianBlur(imagen, (3,3), 0)
    canny = cv2.Canny(gauss, 120, 240)
    kernel=cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2))
    canny = cv2.dilate(canny,kernel,iterations=1)
    
    #BINARIZACIÓN PARA CONTORNOS
    img_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(img_gris, 150, 255, cv2.THRESH_BINARY)
    
    contours,_ =cv2.findContours(canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    image_copy = image.copy()

    cv2.drawContours(image_copy, contours, -20, (255, 0, 200), 1)
    #print("{} CONTOURS FOUNDED".format(len(contours)))
    
    #####################################
    #OTRO CÓDIGO PARA RESOLVERLO CON RETR_TREE
    contornos1,hierarchy = cv2.findContours(th, cv2.RETR_TREE,
               cv2.CHAIN_APPROX_SIMPLE)
     
    cv2.drawContours(imagen, contornos1, -1, (0,255,0), 3)
    
    # print ('len(contornos1[2])=',len(contornos1[2]))
    # print ('len(contornos2[2])=',len(contornos2[2]))
      
    cv2.imshow('Binarizada',th)
    cv2.imshow("Bordes", canny)
    cv2.imshow("Contornos RETR_CCOPM", image_copy)
    cv2.imshow('Contornos RETR_TREE',imagen)
    
    filename = file+"_bordes.jpg"                
    cv2.imwrite(filename, canny)    
    
    filename = file+"_contornos-CCOMP.jpg"                
    cv2.imwrite(filename, image_copy)
    
    filename = file+"contornos-TREE.jpg"                
    cv2.imwrite(filename, imagen)
    
    filename = file+"_segmentacion.jpg"                
    cv2.imwrite(filename, th)
        
    #### CÓDIGO V2
    # image = img
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    # edged = cv2.Canny(blurred, 10, 100)

    # cv2.imshow("Original", image)
    # cv2.imshow("Edged image", edged)

    # contours,_ =cv2.findContours(edged, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # image_copy = image.copy()

    # cv2.drawContours(image_copy, contours, -20, (255, 0, 200), 2)
    # print("{} CONTOURS FOUNDED".format(len(contours)))

    # cv2.imshow("CONTOURS", image_copy)
    # cv2.imshow('Entrada', image) #Muestra la imagen de entrada
    # cv2.calcHist([image],[0],None,[256],[0,256]) #Se calcula el histograma de la imagen de entrada
    # #ravel se usa para cambiar una matriz bidimensional o una matriz multidimensional en una matriz aplanada contigua
    # plt.hist(image.ravel(),256,[0,256])            
    # plt.title('Histograma de entrada') #Titulo del histograma de la imagen de entrada
    # plt.show() #Muestra el histograma de la imagen de entrada

    # # CÓDIGO V1 
    # gris = img
    # gauss = cv2.GaussianBlur(gris, (3,3), 0)
    # canny = cv2.Canny(gauss, 120, 240)
    # kernel=cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2))
    # canny = cv2.dilate(canny,kernel,iterations=1)

    # cv2.imshow("Deteccion de bordes", canny)
    # (contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # msk=np.zeros(canny.shape[:2],np.uint8)
    # cv2.drawContours(msk,contornos,0,(255), -2)
    # new=cv2.bitwise_and(img,img,mask=msk)
    
    # cv2.calcHist([canny],[0],None,[256],[0,256]) #Calcula el histograma de la imagen de salida
    # plt.hist(canny.ravel(),256,[0,256])
    # plt.title('Histograma Bordes') #Titulo del histograma de la imagen de salida
    # plt.show() #Muestra el histograma de la imagen de salida

    # filename = file+"_bordes.jpg"                
    # cv2.imwrite(filename, canny)

    cv2.waitKey(0)
    # global imgN
    # imgN=new
    cv2.destroyAllWindows()
    result.config(text="Detección de Bordes Realizada") #Permite a los usuarios destruir o cerrar todas las ventanas en cualquier momento después de salir del script.

def start(): #Menu de opciones
    if (file == "No se ha seleccionado el archivo") or (file2 == "No se ha seleccionado el archivo"):
        print("No se ha seleccionado el archivo")
        messagebox.showerror(title="Error", message="Inserte una imagen valida")
    else:
        
            try:
                if modo.get() == "Grises":
                    grises(image)
                if modo.get() == "Binarización":
                    binarizacion(image)
                if modo.get() == "Canales BGR":
                    canales(image)
                if modo.get() == "Negativo":
                    negativoImagen(image)
                if modo.get() == "Ecualización Hiperbolica":
                    ecualizacion(image)
                if modo.get() == "Filtro Promedio":
                    promedio(image)
                if modo.get() == "Operador Sobel":
                    sobel(image)
                if modo.get() == "Bordes y Contornos":
                    deteccionBordes(image)
                
            except:
                result.config(text="No se puede realizar esa operación")
                print("No se puede realizar esa operación")

#Función que elige el tipo de imagen y abre un archivo de diálogo
file = ""
def choose():
    global file
    file = filedialog.askopenfilename(filetypes = [
        ("image", ".jfif"),
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    	("image", ".bmp")]) #Lista de tipos de archivos admitidos por este programa
    if len(file) > 0:
        global image
        image = cv2.imread(file)
    fileLabel.configure(text=file)

file2 = ""
def choose2():
    global file2
    file2 = filedialog.askopenfilename(filetypes = [
        ("image", ".jfif"),
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    	("image", ".bmp")]) #Lista de tipos de archivos admitidos por este programa
    if len(file2) > 0:
        global image2
        image2 = cv2.imread(file2)

#Ventana principal
window = Tk()
window.title("PULGONAPP")

window.config(bg = "medium sea green")
window.iconbitmap("./root/icono2.ico")

image = tki.PhotoImage(file="IPN.png")
imageS = image.subsample(6)
widget = tki.Label(image=imageS, bg = "medium sea green")
widget.place(x=-45,y=-4)

image2 = tki.PhotoImage(file="ESCOM.png")
imageS2 = image2.subsample(14)
widget2 = tki.Label(image=imageS2, bg = "medium sea green")
widget2.place(x=440,y=5)
window.geometry("600x500")

lbl = Label(window, text="ESCOM - IPN\n\nSEGMENTACIÓN DE PULGÓN\n\nOperaciones Disponibles\n", font=("Arial", 15), bg = "medium sea green",  anchor="nw")
lbl.place(x=160, y=20)

s = ttk.Style()
s.configure("Peligro.TCombobox", foreground="black", width=20)
s.map("Peligro.TCombobox", foreground=[("active", "#FFA500")])

#Menú para seleccionar la operacion
modo = ttk.Combobox(window, style="Peligro.TCombobox",values=["Grises", "Binarización", "Canales BGR", "Negativo", "Ecualización Hiperbolica","Filtro Promedio", "Operador Sobel", "Bordes y Contornos"],state="readonly")
modo.current(0)
modo.place(x =235,y = 150)

#Boton para cargar imagen
fileButton = Button(window, text="Cargar archivo", command=choose)
fileButton.place(x=255, y=220)
fileButton["bg"] = "#96C7F0"
fileLabel = Label(window, text=file, font=("Arial", 9), bg="light goldenrod", fg="black", width=70)
fileLabel.place(x=55, y=320)
fileLabel.config(anchor=CENTER)


#Boton de accion
btn = Button(window, text="Realizar operacion", command=start)
btn["bg"] = "#96C7F0"
btn.place(x=250, y=440)

result = Label(window, text="", font=("Arial", 12), bg="light goldenrod", fg="black",width=60)
result.place(x=30, y=385)
result.config(anchor=CENTER)

window.mainloop()