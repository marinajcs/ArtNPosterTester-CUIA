# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:38:34 2023

@author: Marina Jun Carranza Sánchez
"""

import speech_recognition as sr

def reconocer_voz():
    texto = ''
    r = sr.Recognizer()
    # Utiliza el micrófono como fuente de audio
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = r.listen(source)

    try:
        # Reconocimiento de voz de Google convierte el audio en texto
        texto = r.recognize_google(audio, language="es-ES")
        
        if texto:
            texto = str.lower(texto)
            print("Texto reconocido:", texto)
        else:
            texto = ''
    except sr.UnknownValueError:
        print("No se pudo reconocer el audio")
        texto = ''
    except sr.RequestError as e:
        print("Error al realizar la solicitud al servicio de reconocimiento de voz:", str(e))

    return texto
