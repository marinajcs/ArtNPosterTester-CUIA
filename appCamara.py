# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:38:34 2023

@author: Marina Jun Carranza Sánchez
"""
import cv2
import numpy as np
from tkinter import filedialog
 
def superponer_logo(frame, logo):
    # Dimensiones de la imagen del logo
    logo_height, logo_width, _ = logo.shape

    # Posición del logo en la esquina superior derecha
    x = frame.shape[1] - logo_width - 10
    y = 10
    roi = frame[y:y+logo_height, x:x+logo_width]

    # Máscara del canal alfa del logo
    logo_alpha = logo[:, :, 3] / 255.0

    # Aplicar la superposición
    for c in range(0, 3):
        frame[y:y+logo_height, x:x+logo_width, c] = \
            logo[:, :, c] * logo_alpha + roi[:, :, c] * (1 - logo_alpha)
            
    return frame
 
def detectar_superficie_color(frame, lower_color, upper_color, imagen_a_insertar):
        # Convierte el frame a espacio de color HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Filtra los colores dentro del rango especificado
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # Aplica operaciones para mejorar la detección
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Encuentra los contornos en la máscara
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Dibuja dichos contornos en la imagen original
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

        # Itera sobre cada contorno y dibuja la imagen dentro del mismo
        for contour in contours:
            # Calcula el rectángulo delimitador del contorno
            x, y, w, h = cv2.boundingRect(contour)

            # Redimensiona la imagen a insertar para que coincida con el tamaño del contorno
            imagen_insertada = cv2.resize(imagen_a_insertar, (w, h))

            # Calcula el ángulo de rotación
            rect = cv2.minAreaRect(contour)
            angle = -rect[2]
            M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
            imagen_insertada_rotada = cv2.warpAffine(imagen_insertada, M, (w, h))

            # Crea una máscara para el contorno
            contour_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            cv2.drawContours(contour_mask, [contour], 0, 255, -1)

            # Aplica la máscara al frame original para borrar el rectángulo negro
            frame= cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(contour_mask))

            # Copia la imagen insertada rotada en la región del contorno en el frame
            frame[y:y+h, x:x+w] = cv2.add(frame[y:y+h, x:x+w], imagen_insertada_rotada)
        
        return frame
