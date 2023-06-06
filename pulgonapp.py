import math
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
from unittest import result
import PIL
from PIL import ImageTk
from PIL import Image
import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt

class SeleccionImagen:
    def __init__(self, master):
        self.master=master
        self.start()
    
    def start(self):
        btn_seleccionarImg=Button(self.master, text="Seleccione una imagen", bg="light goldenrod", fg="black", command=self.seleccionarImagen)
        btn_seleccionarImg.place(x=75,y=25)
    
            
    def seleccionarImagen(self):
        archivo = filedialog.askopenfilename(filetypes=[('Archivos de imagen',"*.jpg")])
        if archivo is not None:
            global imagen, img2
            imagen = Image.open(archivo)
            img2 = cv2.imread(archivo,0)
            x,y = imagen.size
            print(x,y)
            if y>200:
                x=int(x/2.5)
                y=int(y/2.5)
            imagen = imagen.resize((x,y), Image.Resampling.LANCZOS)
            #img2 = cv2.resize(img2, (x,y))
            imagen = ImageTk.PhotoImage(imagen)
            lbl_Img = Label(self.master, image=imagen)
            lbl_Img.image = imagen
            lbl_Img.place(x=3,y=60)
            btn_Erosion1 = Button(self.master, text="Negativo", width=20, bg="light goldenrod", fg="black", command=negativoImagen)
            btn_Erosion1.place(x=(x/3)-25,y=y+70)
            btn_Erosion1 = Button(self.master, text="Gamma", width=20, bg="light goldenrod", fg="black", command=histGamma)
            btn_Erosion1.place(x=(x/3)-25,y=y+100)
            btn_Erosion1 = Button(self.master, text="Segmentar", width=20, bg="light goldenrod", fg="black", command=ErosionarImg1)
            btn_Erosion1.place(x=(x/3)-25,y=y+130)
            btn_Erosion1 = Button(self.master, text="Guardar imagen", width=20, bg="light goldenrod", fg="black", command=GuardarImg1)
            btn_Erosion1.place(x=(x/3)-25,y=y+160)
            #Agregar la función para mostrar el histograma original
            plt.figure('Histograma')
            plt.hist(img2.ravel(), 256, [0, 256])
            plt.title('Histograma Original')
            plt.show()
    
def main():
    root = Tk()
    root.title("SEGMENTACIÓN PULGÓN")
    imagen2 = PhotoImage(file="./root/Fondo3.png")
    root.iconbitmap("./root/icono2.ico")
    lbl_fondo = Label(image=imagen2).place(x=-2,y=10)
    root.geometry("270x420")
    root.resizable(width=True, height=True)
    ventana=SeleccionImagen(root)
    root.mainloop()

def negativoImagen():
    image = cv2.imread("./imagenes/pulgon4.jpg", 0)
    inverted_image = np.invert(image)
    cv2.imwrite("./imagenes/img_invertida.jpg", inverted_image)
    cv2.imshow("Original Image",image)
    cv2.imshow("Inverted Image",inverted_image)
    
    plt.figure('Histograma Inverso')
    plt.hist(inverted_image.ravel(), 256, [0, 256])
    plt.title('Histograma Invertido')
    plt.show()

def histGamma():
    print("Gamma Correction")
    #We take our image to greyscale
    #gray = cv2.GaussianBlur(img2, (3,3), 0)
    gray = img2

    # compute gamma = log(mid*255)/log(mean)
    mid = 0.5
    mean = np.mean(gray)
    gamma = math.log(mid*255)/math.log(mean)
    print(gamma)

    # do gamma correction
    img_gamma1 = np.power(img2, gamma).clip(0,255).astype(np.uint8)

    cv2.imshow('gammaCorrection', img_gamma1)
    cv2.calcHist([img_gamma1],[0],None,[256],[0,256])
    plt.hist(img_gamma1.ravel(),256,[0,256])
    plt.title('Histogram for gamma correction')
    plt.show()

    archivo = archivo+"_gamma.jpg"
    cv2.imwrite(archivo, img_gamma1)

    cv2.waitKey(0)
    global imgNB
    imgNB = imgNB


def ErosionarImg1():
    
    # MÉTODO ANTERIOR 
    gris = img2
    gauss = cv2.GaussianBlur(gris, (3,3), 0)
    canny = cv2.Canny(gauss, 120, 240)
    kernel=cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2))
    canny = cv2.dilate(canny,kernel,iterations=1)

    cv2.imshow("Deteccion de bordes", canny)
    (contornos,_) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    msk=np.zeros(canny.shape[:2],np.uint8)
    cv2.drawContours(msk,contornos,0,(255), -2)
    new=cv2.bitwise_and(img2,img2,mask=msk)
    
    cv2.imshow("Segmentacion",new)
    cv2.drawContours(img2,contornos,0,(255,255,255), 2)
    
    cv2.imshow("Contornos", img2)
    new=imutils.resize(new, width=new.shape[1]*2)
    
    cv2.waitKey(0)
    global imgN
    imgN=new

# AQUI EN VEZ DE imgNB estaba imgN, el cual guardaba la imagen segmentada
def GuardarImg1():
        cv2.imwrite('Segmentacion.png',imgN)
        lblAviso=Label(text="¡Imagen guardada exitosamente!")
        lblAviso.place(x=(imgN.shape[1]/2)+140, y=(imgN.shape[2]/2)+140)

if __name__ == "__main__":
    main()
    