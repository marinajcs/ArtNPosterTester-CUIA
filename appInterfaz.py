# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:38:34 2023

@author: Marina Jun Carranza Sánchez
"""
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk
import shutil
import appCamara as webcam
import appImages as images
import appSpeech as speech
import appRecFacial as faces
import os
import cv2
import numpy as np

texto = ''
predicciones = ""
lower_color = np.array([40, 50, 50])  # Rango inferior de color en formato HSV
upper_color = np.array([80, 255, 255])
frame = None
username = ''
userdir = ''
   
def obtener_color_pixel(event, x, y, flags, param):
    global lower_color, upper_color, frame
    
    if event == cv2.EVENT_LBUTTONDBLCLK:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convierte el frame a espacio de color HSV
        color = hsv[y, x]  # Obtiene el valor HSV del píxel en la posición (x, y)
        # Define el rango inferior y superior de color utilizando un margen
        margen = 40  # Margen de tolerancia para definir el rango
        lower_color = np.array([max(color[0] - margen, 0), max(color[1] - margen, 0), max(color[2] - margen, 0)])
        upper_color = np.array([min(color[0] + margen, 179), min(color[1] + margen, 255), min(color[2] + margen, 255)])

def cargar_imagen(audio):
    if images.abrir_imagen(userdir):
        if audio == True:
            abrir_galeria("visualizar", True)
        else:
            abrir_galeria("visualizar", False)

def identificar_imagen(audio):
    if audio == True:
        abrir_galeria("identificar", True)
    else:
        abrir_galeria("identificar", False)

def buscar_imagen(audio):
    if audio == True:
        texto = ''
        while texto == '':
            texto = speech.reconocer_voz()
            # texto = "gatos" (ejemplo)
        images.obtener_imagen_busqueda(userdir, texto)
        abrir_galeria("visualizar", True)
    else:
        root = tk.Tk()
        root.withdraw()
        nombre_buscar = simpledialog.askstring("Nombre", "Por favor, introduce el nombre del fichero a buscar")
        images.obtener_imagen_busqueda(userdir, nombre_buscar)
        abrir_galeria("visualizar", False)
    
def comandos_voz():
    instrucc.pack(pady=10)
    texto = ''
    
    while texto == '':
        texto = speech.reconocer_voz()
        
        if texto == "cargar imagen":
            cargar_imagen(True)
        elif texto == "identificar imagen":
            identificar_imagen(True)
        elif texto == "buscar imagen":
            buscar_imagen(True)
        elif texto == "abrir cámara":
            abrir_camara(True)
        elif texto == "abrir galería":
            abrir_galeria("visualizar", True)
        elif texto == "cerrar sesión":
            cerrar_sesion()
        elif texto == "cerrar ventana":
            root.destroy()
        elif texto == "eliminar usuario":
            eliminacion_user("personal")
        else:
            print("Orden no disponible")
            texto = ''

         
def abrir_camara(audio):
    if audio == True:
        abrir_galeria("seleccionar", True)
    else:
        abrir_galeria("seleccionar", False)
    

def ejecucionCamara(ruta_img, audio):
    global frame, lower_color, upper_color
    imagen = cv2.imread(ruta_img, cv2.IMREAD_UNCHANGED)
    logo_cv = cv2.imread("./icons/logo_transp.png", cv2.IMREAD_UNCHANGED)
    logo_width_deseado = 100
    proporcion = logo_width_deseado / logo_cv.shape[1]
    logo_cv = cv2.resize(logo_cv, (int(logo_cv.shape[1] * proporcion), int(logo_cv.shape[0] * proporcion)))

    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Obtener Rango de Color del Pixel')
    cv2.setMouseCallback('Obtener Rango de Color del Pixel', obtener_color_pixel)

    if not cap.isOpened():
        print("No se puede abrir la cámara")
        exit()
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("No he podido leer el frame")
            break

        # Aplica la detección de sperficies de color al frame actual
        resultado = webcam.detectar_superficie_color(frame, lower_color, upper_color, imagen)
        resultado = cv2.flip(resultado, 1)
        resultado = webcam.superponer_logo(resultado, logo_cv)

        # Muestra el resultado en tiempo real
        cv2.imshow('Obtener Rango de Color del Pixel', resultado)
            
        if cv2.waitKey(1) == ord(' '):# or txt == "cerrar ventana":
            break

    cap.release()
    cv2.destroyWindow('Obtener Rango de Color del Pixel')
    
    if audio == True:
        print("¿Nueva orden?")
        comandos_voz()

def abrir_galeria(opcion, audio):
    if os.path.isdir(userdir):
        archivos = os.listdir(userdir)
        n = 0
        print("Lista de imgs:")
        for archivo in archivos:
            n += 1
            print(str(n) + ") " + archivo)
    else:
        print("La ruta no es una carpeta válida.")
    
    ventana = tk.Toplevel(root)
    vt = "Galería de " + username
    ventana.title(vt)
    ventana.geometry("650x500")
    
    if opcion == "visualizar" and audio == True:
        txt = "Para eliminar una imagen, diga el nombre del fichero (sin extensión)\n en voz alta una vez se haya cerrado esta ventana (7s).\nSi desea ejecutar otra orden, diga 'nueva orden' y después, el comando a realizar."
        instrucc = ttk.Label(ventana, text=txt, style='TLabel')
        instrucc.pack(pady=10)
    elif opcion == "seleccionar" and audio == True:
        txt = "Para seleccionar una imagen, diga el nombre del fichero (sin extensión)\n en voz alta una vez se haya cerrado esta ventana (7s).\nSi desea ejecutar otra orden, diga 'nueva orden' y después, el comando a realizar."
        instrucc = ttk.Label(ventana, text=txt, style='TLabel')
        instrucc.pack(pady=10)
    elif opcion == "identificar" and audio == True:
        txt = "Para identificar una imagen, diga el nombre del fichero (sin extensión)\n en voz alta una vez se haya cerrado esta ventana (7s).\nSi desea ejecutar otra orden, diga 'nueva orden' y después, el comando a realizar."
        instrucc = ttk.Label(ventana, text=txt, style='TLabel')
        instrucc.pack(pady=10)

    # Crear un frame para el contenido de la galería
    frame_contenedor = tk.Frame(ventana)
    frame_contenedor.pack(fill=tk.BOTH, expand=True)
    
    canvas = tk.Canvas(frame_contenedor)
    scrollbar = tk.Scrollbar(frame_contenedor, orient=tk.VERTICAL, command=canvas.yview)
    canvas.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    frame_interno = tk.Frame(canvas)
    frame_interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=frame_interno, anchor=tk.NW)
    
    imagenes = []
    n = 0
    for archivo in os.listdir(userdir):
        n += 1
        ruta_archivo = os.path.join(userdir, archivo)
        if os.path.isfile(ruta_archivo):
            try:
                imagen = Image.open(ruta_archivo)
                imagen = imagen.resize((125, 125))  # Redimensionar todas las imágenes a un tamaño fijo
                img_tk = ImageTk.PhotoImage(imagen)
                imagenes.append((img_tk, n, archivo, ruta_archivo))  # Almacenar la imagen y el nombre del archivo
            except Exception as e:
                print(f"No se pudo cargar la imagen {ruta_archivo}: {str(e)}")

    num_columnas = 4
    
    for i, (img_tk, n, fname, ruta) in enumerate(imagenes):
        # Calcular las coordenadas de la celda actual en la cuadrícula
        fila = i // num_columnas
        columna = i % num_columnas

        # Crear un marco para contener la imagen y el texto
        frame = tk.Frame(frame_interno)
        frame.grid(row=fila, column=columna, padx=10, pady=10)

        # Crear etiqueta de imagen
        label_imagen = tk.Label(frame, image=img_tk)
        label_imagen.image = img_tk  # Mantener referencia a la imagen
        label_imagen.pack()
        if opcion == "visualizar" and audio == False:
            boton_eliminar = tk.Button(frame, text="Eliminar", command=lambda ruta=ruta: eliminar_imagen(ruta, False, "galeria", '', boton_eliminar))
            boton_eliminar.pack()
        elif opcion == "seleccionar" and audio == False:
            boton_selecc = tk.Button(frame, text="Seleccionar", command=lambda ruta=fname: seleccionar_imagen(ruta, "seleccionar", False))
            boton_selecc.pack()
        elif opcion == "identificar" and audio == False:
            boton_selecc = tk.Button(frame, text="Seleccionar", command=lambda ruta=fname: seleccionar_imagen(ruta, "identificar", False))
            boton_selecc.pack()
            
        # Crear etiqueta de texto con el nombre del archivo
        titulo = str(n) + ") " + fname
        label_nombre = tk.Label(frame, text=titulo)
        label_nombre.pack()
        
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    frame_contenedor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    if audio == True:
        ventana.after(7000, lambda: ventana.destroy())
        
    # Espera a que se cierre la ventana antes de ejecutar el código siguiente
    ventana.wait_window()
    
    if audio == True:
        nombre_arch = ''
        print("¿Nombre del archivo?")
        nombre_arch = speech.reconocer_voz()
            
        ruta_arch = ''
        encontrado = False
        nueva_orden = False
        
        while encontrado == False and nueva_orden == False:
            if nombre_arch == "nueva orden":
                nueva_orden = True
                break
            else:
                for img_tk, n, fname, ruta in imagenes:
                    nombre, ext = os.path.splitext(fname) # Para quitar extensión img.jpg
                    if nombre == nombre_arch:
                        ruta_arch = ruta
                        print("Archivo encontrado en " + ruta_arch)
                        encontrado = True
                        break
                else:
                    print("No se encontró ningún archivo con dicho nombre. Pruebe con otro.")
                    nombre_arch = ''
                    print("¿Nombre del archivo?")
                    nombre_arch = speech.reconocer_voz()
                    
        if nueva_orden == True:
            print("¿Nueva orden?")
            comandos_voz()
            
        if encontrado == True and ruta_arch != '':
            if opcion == "visualizar":
                eliminar_imagen(ruta_arch, True, "galeria", '', instrucc)    
            elif opcion == "seleccionar": 
                seleccionar_imagen(fname, "seleccionar", True)
            elif opcion == "identificar":        
                seleccionar_imagen(fname, "identificar", True)
                

def eliminar_imagen(ruta, audio, opc, nom_galeria, boton):
    try:
        os.remove(ruta)  # Eliminar el archivo de la ruta especificada

        if opc == "galeria":
            if audio == True:
                abrir_galeria("visualizar", True) # Regenerar la galería actualizada
            else:
                abrir_galeria("visualizar", False)
        else: # if opc == "usuarios". Para manejar borrado de usuario
            nom_gal, ext = os.path.splitext(nom_galeria) # Para quitar extensión img.jpg
            ruta_galeria = os.path.join("galerias", nom_gal)
            try:
                shutil.rmtree(ruta_galeria)
                print("Galería de " + nom_gal + " eliminada exitosamente")
            except OSError as e:
                print("No se pudo eliminar la galería correctamente")
            
            eliminacion_user("admin")
    except Exception as e:
        print(f"No se pudo eliminar la imagen {ruta}: {str(e)}")
        
        
def seleccionar_imagen(ruta, opc, audio):
    print("Imagen seleccionada:", ruta)
    ruta = "./galerias/" + username + "/" + ruta
    if opc == "seleccionar":
        ejecucionCamara(ruta, audio)
    elif opc == "identificar":
        # Carga la imagen seleccionada
        ven = tk.Toplevel(root)
        ven.title("Identifica imagen: " + ruta)
        predicciones = ""
        imagen = Image.open(ruta)
        imagen = imagen.resize((150, 150))
        
        img_tk = ImageTk.PhotoImage(imagen)
        label_imagen = tk.Label(ven, image=img_tk)
        label_imagen.image = img_tk  # Mantener referencia a la imagen
        label_imagen.pack()
        
        predictions = images.reconocer_imagen(ruta)
        n = 0
        for prediction in predictions:
            n += 1
            objeto = prediction[1]
            probabilidad = prediction[2] * 100
            predicciones += "------------------------\n"
            predicciones += "Predicc. #" + str(n) + "\n"
            predicciones += "Objeto: " + objeto + "\n"
            predicciones += "Probabilidad: " + str(probabilidad) + "%\n"
            
        print(predicciones)
        # Crear un widget de etiqueta para mostrar el texto
        etiqueta = tk.Label(ven, text=predicciones)
        etiqueta.pack()
        
        if audio == True:
            ven.after(7000, lambda: ven.destroy())
            
            ven.wait_window()
            print("¿Nueva orden?")
            comandos_voz()
    

def cambiar_estado():
    if boton_estado.get(): # Botón activado
        print("Interfaz sin audio activada")
        for boton in botones_ocultos:
            boton.pack(pady=10)
            
        boton_audio.pack_forget()
    else: # Botón desactivado
        print("Interfaz sin audio desactivada")
        for boton in botones_ocultos:
            boton.pack_forget()
        
        boton_audio.pack(pady=10)


def identificacion_user():
    global username, userdir
    username = faces.reconocimiento_facial()
    ruta_directorio = os.path.join("galerias", username)
    # Verificar si la galería ya existe (usuario se ha registrado anteriormente)
    if not os.path.exists(ruta_directorio):
        os.mkdir(ruta_directorio)
        print("Galería creada exitosamente.")
    else:
        print("La galería ya existe.")
        
    userdir = ruta_directorio
    print(userdir)
    
    boton_ventana0.pack_forget()
    boton_ventana00.pack_forget()
    bienv1.pack_forget()
    
    # Una vez terminada la identificación, muestra el resto de funciones
    bienvenida2 = "¡Bienvenido/a a la aplicación, " + username + "!"
    bienv2.configure(text=bienvenida2)
    bienv2.pack(pady=20)
    boton_not_audio.pack(pady=10)
    boton_audio.pack(pady=10)
    boton_logout.pack(pady=10)
    boton_elim_user.pack(pady=3)
    
def cerrar_sesion():
    global username, userdir
    username = ''
    userdir = ''
    bienv1.pack(pady=20)
    boton_ventana0.pack(pady=10)
    boton_ventana00.pack(pady=10)
    
    instrucc.pack_forget()
    bienv2.pack_forget()
    boton_not_audio.pack_forget()
    boton_audio.pack_forget()
    if boton_estado.get(): # Botón audio activado
        for boton in botones_ocultos:
            boton.pack_forget()
        
    boton_logout.pack_forget()
    boton_elim_user.pack_forget()
    
def eliminacion_user(opc):
    if opc == "admin":
        ventana = tk.Toplevel()
        vt = "Lista de usuarios registrados"
        ventana.title(vt)
        
        # Crear un frame para el contenido de las listas
        frame_contenedor = tk.Frame(ventana)
        frame_contenedor.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(frame_contenedor)
        scrollbar = tk.Scrollbar(frame_contenedor, orient=tk.VERTICAL, command=canvas.yview)
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        frame_interno = tk.Frame(canvas)
        frame_interno.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame_interno, anchor=tk.NW)

        usuarios = []
        n = 0
        for archivo in os.listdir("./faces"):
            n += 1
            ruta_archivo = "./faces/" + archivo
            if os.path.isfile(ruta_archivo):
                try:
                    imagen = Image.open(ruta_archivo)
                    imagen = imagen.resize((125, 125))  # Redimensionar todas las imágenes a un tamaño fijo
                    img_tk = ImageTk.PhotoImage(imagen)
                    usuarios.append((img_tk, n, archivo, ruta_archivo))  # Almacenar la imagen y el nombre del archivo
                except Exception as e:
                    print(f"No se pudo cargar la imagen {ruta_archivo}: {str(e)}")
                    
        num_columnas = 4

        for i, (img_tk, n, fname, ruta) in enumerate(usuarios):
            # Calcular las coordenadas de la celda actual en la cuadrícula
            fila = i // num_columnas
            columna = i % num_columnas
            
            # Crear un marco para contener la imagen y el texto
            frame = tk.Frame(frame_interno)
            frame.grid(row=fila, column=columna, padx=10, pady=10)
            
            # Crear etiqueta de imagen
            label_imagen = tk.Label(frame, image=img_tk)
            label_imagen.image = img_tk  # Mantener referencia a la imagen
            label_imagen.pack()
            boton_eliminar = tk.Button(frame, text="Eliminar", command=lambda ruta=ruta: eliminar_imagen(ruta, False, "usuarios", fname, boton_eliminar))
            boton_eliminar.pack()
            
            # Crear etiqueta de texto con el nombre del usuario
            titulo = str(n) + ") " + fname
            label_nombre = tk.Label(frame, text=titulo)
            label_nombre.pack()
            
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame_contenedor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ventana.mainloop()
    else: # opc == "personal"
        img = username + ".jpg"
        ruta_img = os.path.join("faces", img)
        os.remove(ruta_img)  # Eliminar la imagen del usuario
        ruta_galeria = os.path.join("galerias", username)
        try:
            shutil.rmtree(ruta_galeria) # Eliminar la galería también
            print("Galería de " + username + " eliminada exitosamente")
        except OSError as e:
            print("No se pudo eliminar la galería correctamente")
            
        cerrar_sesion()
            

# Creación de la ventana principal
root = tk.Tk()
root.title("Aplicación CUIA")

logo_app = Image.open("./icons/logo_cuia.png")
logo_app = logo_app.resize((170, 130))
logo = ImageTk.PhotoImage(logo_app)
label_logo = tk.Label(root, image=logo)
label_logo.image = logo
label_logo.pack()

# Estilo para los elementos
style = ttk.Style()
style.configure('TButton', font=('Trebuchet MS', 12))
style.configure('TLabel', font=('Trebuchet MS', 15))
style.configure('TFrame', background="white")

# Contenedor principal
main_frame = ttk.Frame(root)
main_frame.pack()
main_frame.configure(style="TFrame")

boton_estado = tk.BooleanVar()

bienvenida1 = "¡Bienvenido/a a la aplicación! ¿Procedemos con la identificación de usuario?"
bienv1 = ttk.Label(main_frame, text=bienvenida1, style='TLabel')
bienv1.pack(pady=20)

boton_ventana0 = ttk.Button(main_frame, text="Adelante :D", command=identificacion_user)
boton_ventana0.pack(pady=10)
boton_ventana00 = ttk.Button(main_frame, text="Eliminar usuarios", command=lambda: eliminacion_user("admin"))
boton_ventana00.pack(pady=10)

bienvenida2 = "¡Bienvenido/a a la aplicación, " + username + "!"
bienv2 = ttk.Label(main_frame, text=bienvenida2, style='TLabel')

not_audio_icono = Image.open("./icons/not_audio.png")
not_audio_icono = not_audio_icono.resize((50, 50))
icono1 = ImageTk.PhotoImage(not_audio_icono)
boton_not_audio = tk.Checkbutton(main_frame, image=icono1, variable=boton_estado, command=cambiar_estado)

# Botones para abrir las ventanas
boton_ventana1 = ttk.Button(main_frame, text="Cargar imagen", command=lambda: cargar_imagen(False))
boton_ventana2 = ttk.Button(main_frame, text="Identificar imagen", command=lambda: identificar_imagen(False))
boton_ventana3 = ttk.Button(main_frame, text="Buscar imagen", command=lambda: buscar_imagen(False))
boton_ventana4 = ttk.Button(main_frame, text="Abrir cámara", command=lambda: abrir_camara(False))
boton_ventana5 = ttk.Button(main_frame, text="Abrir galería", command=lambda: abrir_galeria("visualizar", False))

botones_ocultos = [boton_ventana1, boton_ventana2, boton_ventana3, boton_ventana4, boton_ventana5]

audio_icono = Image.open("./icons/audio.png")
audio_icono = audio_icono.resize((50, 50))
icono2 = ImageTk.PhotoImage(audio_icono)

boton_audio = ttk.Button(main_frame, image=icono2, command=comandos_voz)

txt = "Lista de órdenes posibles: cargar imagen, identificar imagen, buscar imagen, abrir cámara,\nabrir galería, cerrar sesión y cerrar ventana."
instrucc = ttk.Label(main_frame, text=txt, style='TLabel')

boton_logout = ttk.Button(root, text="Cerrar sesión", command=cerrar_sesion)
boton_elim_user = ttk.Button(root, text="Eliminar usuario", command=lambda: eliminacion_user("personal"))

etiqueta_imagen = tk.Label(root)
etiqueta_imagen.pack()

etiqueta_texto = tk.Label(root)
etiqueta_texto.pack()

# Ejecución del bucle principal de la app
root.mainloop()