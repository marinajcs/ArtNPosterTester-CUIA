# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:38:34 2023

@author: Marina Jun Carranza Sánchez
"""

import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
import urllib.parse
import os

model = ResNet50(weights='imagenet')

def abrir_imagen(userdir):
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.tif")])

    if ruta_imagen:
        # Carga la imagen seleccionada
        imagen = Image.open(ruta_imagen)
        # Guarda la imagen en un archivo
        nombre_guardado = filedialog.asksaveasfilename(defaultextension="png",
                                                       filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.tif")],
                                                       initialdir=userdir,
                                                       initialfile="nombre_archivo.png")
        if nombre_guardado:
            # Guarda la imagen en el nombre de archivo especificado en el directorio actual
            imagen.save(nombre_guardado)
        return True
    
    return False

def reconocer_imagen(ruta_imagen):
    # Cargar la imagen
    img = image.load_img(ruta_imagen, target_size=(224, 224))
    img = image.img_to_array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)

    # Realizar la predicción utilizando el modelo
    preds = model.predict(img)
    predictions = decode_predictions(preds, top=7)[0]
 
    return predictions


def obtener_imagen_busqueda(userdir, texto):
    # Codificar el texto de búsqueda para formar la URL
    texto_codificado = urllib.parse.quote(texto)
    # Credenciales de mi Custom Search API (Google)
    api_key = 'AIzaSyADHGZoCrKOdS1PEv1EG0dwF3gK8coI6N4'
    cx = '24a8d01b641c4439d'
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={texto_codificado}&searchType=image"
    
    try:
        # Realizar la solicitud a la API de búsqueda de imágenes de Google
        response = requests.get(url)
        response.raise_for_status()
        
        # Extraer la URL de la primera imagen encontrada
        datos = response.json()
        if "items" in datos and len(datos["items"]) > 0:
            url_imagen = datos["items"][0]["link"]

            # Descargar la imagen
            nombre_imagen = texto_codificado + ".jpg"
            os.makedirs(userdir, exist_ok=True)
            ruta_imagen = os.path.join(userdir, nombre_imagen)
            
            response = requests.get(url_imagen)
            response.raise_for_status()
            
            with open(ruta_imagen, "wb") as archivo:
                archivo.write(response.content)
            
            print(f"Imagen descargada: {ruta_imagen}")
        
        else:
            print("No se encontró ninguna imagen en la búsqueda.")
        
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error al realizar la búsqueda de imágenes: {e}")



