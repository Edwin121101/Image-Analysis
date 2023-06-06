import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageOps, ImageEnhance


class ImageProcessor:

    def __init__(self, root):

        self.root = root
        self.root.title("Procesador de Imágenes")
        self.root.resizable(width=True, height=True)

        # Variables para los parámetros de las operaciones
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.brightness_var = tk.IntVar(value=0)
        self.gaussian_var = tk.IntVar(value=3)
        self.laplacian_var = tk.IntVar(value=1)
        # Variable para el negativo de la imagen
        self.black = 0

        # Interfaz gráfica
        # padx: padding en el eje x 
        # pady: padding en el eje y
        # sticky: alineación del elemento N, S, E, W
        # columnspan: número de columnas que ocupa el elemento
        # rowspan: número de filas que ocupa el elemento
        # command: Funcion que ejecuta 

        tk.Label(self.root, text="Seleccionar imagen:").grid(row=0, column=0, padx=10, pady=10)
        self.filename_label = tk.Label(self.root, text="")
        self.filename_label.grid(row=0, column=1, padx=10, pady=10)

        self.select_button = tk.Button(self.root, text="Seleccionar", command=self.select_image)
        self.select_button.grid(row=0, column=2, padx=10, pady=10)

        tk.Label(self.root, text="Contracción del histograma:").grid(row=1, column=0, padx=10, pady=10)
        self.contrast_slider = tk.Scale(self.root, from_=0.1, to=10.0, resolution=0.1, orient=tk.HORIZONTAL,
                                        variable=self.contrast_var)
        self.contrast_slider.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Brillo:").grid(row=2, column=0, padx=10, pady=10)
        self.brightness_slider = tk.Scale(self.root, from_=0, to=510, resolution=1, orient=tk.HORIZONTAL,
                                          variable=self.brightness_var, command=self.change_brightness)
        self.brightness_slider.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Filtro Gaussiano:").grid(row=3, column=0, padx=10, pady=10)
        self.gaussian_slider = tk.Scale(self.root, from_=1, to=11, resolution=2, orient=tk.HORIZONTAL,
                                        variable=self.gaussian_var)
        self.gaussian_slider.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Filtro Laplaciano:").grid(row=4, column=0, padx=10, pady=10)
        self.laplacian_slider = tk.Scale(self.root, from_=1, to=5, resolution=1, orient=tk.HORIZONTAL,
                                         variable=self.laplacian_var)
        self.laplacian_slider.grid(row=4, column=1, padx=10, pady=10)

        self.negative_button = tk.Button(self.root, text="Negativo", command=self.apply_negative)
        self.negative_button.grid(row=5, column=2, padx=10, pady=10)

        self.black_white_button = tk.Button(self.root, text="Black&White", command=self.apply_black_white)
        self.black_white_button.grid(row=5, column=3, padx=10, pady=20)

        self.process_button = tk.Button(self.root, text="Procesar imagen", command=self.process_image)
        self.process_button.grid(row=5, column=1, padx=10, pady=10)

        self.save_button = tk.Button(self.root, text="Guardar imagen", command=self.save_image)
        self.save_button.grid(row=7, column=1, padx=10, pady=10)

        # Boton RGB
        self.show_channels_button = tk.Button(self.root, text="Mostrar canales RGB", command=self.show_RGB_channels)
        self.show_channels_button.grid(row=7, column=1, padx=10, pady=10)

        # Imagen a ser editada
        self.image_frame = tk.Frame(self.root)
        self.image_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
        self.image_label_title = tk.Label(self.image_frame, text="Imagen procesada:")
        self.image_label_title.pack(side="top")
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(side="bottom")



        # Canal RED
        self.image_frameRED = tk.Frame(self.root)
        self.image_frameRED.grid(row=6, column=3, columnspan=3, padx=10, pady=10)
        self.image_label_title_RED = tk.Label(self.image_frameRED, text="Canal R:")
        self.image_label_title_RED.pack(side="top")
        self.image_labelR = tk.Label(self.image_frameRED)
        self.image_labelR.pack(side="bottom")


        # Canal GREEN
        self.image_frameGREEN = tk.Frame(self.root)
        self.image_frameGREEN.grid(row=6, column=6, columnspan=3, padx=10, pady=10)
        self.image_label_title_GREEN = tk.Label(self.image_frameGREEN, text="Canal G:")
        self.image_label_title_GREEN.pack(side="top")
        self.image_labelG = tk.Label(self.image_frameGREEN)
        self.image_labelG.pack(side="bottom")


        # Canal BLUE
        self.image_frameBLUE = tk.Frame(self.root)
        self.image_frameBLUE.grid(row=6, column=9, columnspan=3, padx=10, pady=10)
        self.image_label_title_BLUE = tk.Label(self.image_frameBLUE, text="Canal B:")
        self.image_label_title_BLUE.pack(side="top")
        self.image_labelB = tk.Label(self.image_frameBLUE)
        self.image_labelB.pack(side="bottom")



        # Imagen Original
        self.original_image = None
        self.original_image_label = tk.Label(self.root)
        self.original_image_label.grid(row=0, column=6, rowspan=6, padx=10, pady=10)

    # Funcion para salvar la imagen modificada
    def save_image(self):
        if hasattr(self, 'original_image'):
            # Obtener la imagen procesada
            image = ImageTk.getimage(self.image_label.image)
            # Abrir el diálogo para guardar la imagen
            file_path = filedialog.asksaveasfilename(defaultextension='.png')
            # Guardar la imagen
            image.save(file_path)

    # Aplicando escala de grises
    def apply_black_white(self):
        if hasattr(self, 'original_image'):
            if self.black == 1:
                self.black_white_button.config(background="red")
                self.black = 0
            else:
                self.black_white_button.config(background="green")
                self.black = 1

    # Cambiando el brillo (La función se ejecuta cada que se mueve el slider)
    def change_brightness(self, event=None):
        if hasattr(self, 'original_image'):
            # Obtener la imagen original
            image = self.original_image.copy()
            # Obtener el valor del slider
            slider_value = self.brightness_var.get()
            # Aplicar el brillo
            brightness = ImageEnhance.Brightness(image)
            image = brightness.enhance(slider_value / 255)
            # Mostrar la imagen con el negativo aplicado
            photo_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo_image)
            self.image_label.image = photo_image

    # TODO Aqui falta hacerlo pero con la imagen que actualmente se esta modificando
    def apply_negative(self):
        if hasattr(self, 'original_image'):
            # Obtener la imagen original
            image = self.original_image
            # Aplicar el negativo
            image = ImageOps.invert(image)

            # Mostrar la imagen con el negativo aplicado
            photo_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo_image)
            self.image_label.image = photo_image

    def select_image(self):
        # Abrir el diálogo de selección de archivo
        filename = filedialog.askopenfilename(initialdir="/", title="Seleccionar imagen",
                                              filetypes=(("Archivos de imagen", "*.jpg;*.jpeg;*.png"),
                                                         ("Todos los archivos", "*.*")))
        if filename:
            # Mostrar la ruta del archivo seleccionado
            self.filename_label.config(text=filename)

            # Cargar la imagen seleccionada
            image = Image.open(filename)
            # Cambiando tamaño para poder visualizar mejor
            # TODO no se si sea correcto cambiar el tamaño por la profa
            image.thumbnail((400, 400))

            # Mostrar la imagen que se va a modificar
            photo_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo_image)
            self.image_label.image = photo_image

            # Mostrar la imagen original
            self.original_image_label.config(image=photo_image)
            self.original_image_label.image = photo_image

            self.image_labelR.config(image=photo_image)
            self.image_labelR.image = photo_image

            self.image_labelG.config(image=photo_image)
            self.image_labelG.image = photo_image

            self.image_labelB.config(image=photo_image)
            self.image_labelB.image = photo_image

            # Guardar la imagen original para restaurarla después de procesar la imagen
            self.original_image = image

    def process_image(self):
        if hasattr(self, 'original_image'):
            # Obtener la imagen original
            image = self.original_image.copy()

            # Aplicar la contracción y expansión del histograma
            image = ImageOps.autocontrast(image, self.contrast_var.get())

            # Aplicar el filtro Gaussiano
            image = image.filter(ImageFilter.GaussianBlur(radius=self.gaussian_var.get()))

            # Aplicar el filtro Laplaciano
            for i in range(self.laplacian_var.get()):
                image = image.filter(ImageFilter.Kernel((3, 3), [-1, -1, -1, -1, 9, -1, -1, -1, -1]))

            # Aplicar los negativos
            # image = ImageOps.invert(image)

            # Ajustar el brillo
            slider_value = self.brightness_var.get()

            brightness = ImageEnhance.Brightness(image)

            # Aplicar el negativo
            image = brightness.enhance(slider_value / 255)

            if self.black == 1:
                # Aplicar el negativo
                image = ImageOps.grayscale(image)

                # Mostrar la imagen con el negativo aplicado
                photo_image = ImageTk.PhotoImage(image)

            # Mostrar la imagen procesada
            photo_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo_image)
            self.image_label.image = photo_image

    def show_RGB_channels(self):
        if hasattr(self, 'original_image'):
            # Obtener los canales RGB
            red_channel, green_channel, blue_channel = self.original_image.split()

            # Mostrar los canales RGB en cada ventana
            red_image = ImageTk.PhotoImage(red_channel)
            green_image = ImageTk.PhotoImage(green_channel)
            blue_image = ImageTk.PhotoImage(blue_channel)

            self.image_labelR.config(image=red_image)
            self.image_labelR.image = red_image

            self.image_labelG.config(image=green_image)
            self.image_labelG.image = green_image

            self.image_labelB.config(image=blue_image)
            self.image_labelB.image = blue_image


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()
