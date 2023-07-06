# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:38:34 2023

@author: Marina Jun Carranza Sánchez
"""
import cv2
import face_recognition
import os
import tkinter as tk
from tkinter import simpledialog

def obtener_nombre_usuario():
    root = tk.Tk()
    root.withdraw()
    nombre_usuario = simpledialog.askstring("Nombre", "Por favor, introduce tu nombre:")
    return nombre_usuario

def cargar_caras_registradas():
    caras_registradas = {}
    for archivo in os.listdir('./faces'):
        nombre = os.path.splitext(archivo)[0]
        ruta_archivo = os.path.join('faces', archivo)
        imagen = face_recognition.load_image_file(ruta_archivo)
        codificaciones = face_recognition.face_encodings(imagen)
        if len(codificaciones) > 0:
            codificacion = codificaciones[0]
            caras_registradas[nombre] = codificacion
        else:
            print(f"No se detectaron caras en el archivo: {archivo}")
    return caras_registradas

def reconocimiento_facial():
    nombre_usuario = ''
    cam = cv2.VideoCapture(0)
    
    # Clasificador de cascada para detectar caras
    cascada_cara = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Leer las caras registradas en la carpeta 'faces'
    caras_registradas = cargar_caras_registradas()
    
    while True:
        ret, frame = cam.read()
        
        # Convertir imagen a escala de grises, detectar caras en la imagen y dibujar rectángulo verde alrededor de ellas
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        caras = cascada_cara.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in caras:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        cv2.imshow('Detector de caras', frame)
        
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
        
        # Convertir la imagen a RGB para la detección de caras
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detectar las ubicaciones de las caras en la imagen y codificarlas
        ubicaciones = face_recognition.face_locations(rgb_frame)
        codificaciones = face_recognition.face_encodings(rgb_frame, ubicaciones)
        
        # Comprobar si alguna de las caras detectadas coincide con las caras registradas
        cara_identificada = False
        for codificacion in codificaciones:
            for nombre, encoding in caras_registradas.items():
                coincidencias = face_recognition.compare_faces([encoding], codificacion)
                
                # Si hay una coincidencia, se ha identificado la cara
                if coincidencias[0]:
                    cara_identificada = True
                    nombre_usuario = nombre
                    break
            
            if cara_identificada:
                break
            
        # Si se detectó una cara ya identificada...
        if cara_identificada:
            print(f"Bienvenido/a de nuevo, {nombre_usuario}")
            break
        
        # Si se detectó una cara no identificada, guardar la imagen en la carpeta 'caras'
        if len(caras) > 0:
            nombre_usuario = obtener_nombre_usuario()
            ruta_archivo = os.path.join('faces', f'{nombre_usuario}.jpg')
            cv2.imwrite(ruta_archivo, frame)
            print(f"Nuevo/a usuario/a registrado/a en: {ruta_archivo}")
            break
    
    cam.release()
    cv2.destroyAllWindows()
    
    return nombre_usuario

