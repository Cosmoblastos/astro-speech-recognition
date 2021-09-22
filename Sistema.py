'''
	Este codigo contiene el administrador de operaciones mediante comando de voz
'''

import Tex_Spe  as TS
import Spe_Text as ST
import subprocess
import os
import time
#import ComandsQ
from redis import Redis
import json

#Esta funcion utiliza 35 subprocesos para identificar si se ha mencionando el nombre del asistente 
def Llamado(Nombre):  

	child0 = subprocess.Popen(['python', './Auxiliar.py'])
	time.sleep(0.2)
	child1 = subprocess.Popen(['python', './Auxiliar.py'])
	time.sleep(0.2)
	child2 = subprocess.Popen(['python', './Auxiliar.py'])
	time.sleep(0.2)
	child3 = subprocess.Popen(['python', './Auxiliar.py'])
	time.sleep(0.2)
	child4 = subprocess.Popen(['python', './Auxiliar.py'])

	while(child0.poll() == None and child1.poll() == None and child2.poll() == None and child3.poll() == None and child4.poll() == None): 
		pass

	try: child0.kill()
	except: pass
	try: child1.kill()
	except: pass
	try: child2.kill()
	except: pass
	try: child3.kill()
	except: pass
	try: child4.kill()
	except: pass


def main ():
	Encendido = True           #Este es el estao de astro
	Nombre = 'Astro'
	TTS1 = TS.TTS()
	r=Redis(host="localhost",port=6379)
	#.................................................................................................................
	#Inicia el protocolo para escuchar a diestra y siniestra
	while (Encendido == True):

		#Instruccion para detectar el nombre del asistente
		Llamado(Nombre)

		#Escuchamos la instruccion
		Duracion = 4 
		Spe_Text = ST.STT()
		print("\n\n Te escucho ........ \n\n")
		r.rpush("voiceEvents", json.dumps({'type': "event", "name": "hearing"}, indent = 4))
		Texto = Spe_Text.Lisen(Duracion)
		print(Texto)
		
		if not Texto: continue

		Intentos = 0
		Success = False
		while(Intentos<3 and Success == False):

			if(Texto=="apagar"):
				Success = True
				Encendido = False

			if(Texto=="hora"):
				os.system("python Hora.py")
				Success = True

			if (Texto == "presentate" or Texto == "preséntate"):
				TTS1.Speak(Texto="Hola, soy ASTRO, tu asistente médico personal")
				Success = True

			if "google" in Texto:
				Consulta = Texto.replace("google","")
				os.system("python google.py " + Consulta)
				Success = True

			if "emergencia" in Texto:
				#PREGUNTA ¿qué edad tiene?
				TTS1.Speak(Texto="¿Qué edad tiene el paciente?")
				# ----ASTRO escucha y almacena el texto
				edad = Spe_Text.Lisen(Duracion=5)
				#PREGUNTA ¿es hombre o mujer?
				TTS1.Speak(Texto="¿Es hombre o mujer?")
				# ----ASTRO escucha y almacena el texto
				sexo = Spe_Text.Lisen(Duracion=5)
				
				#Se muestra el video en la interfaz gráfica y avanza ASTRO al paciente
				#---TAREA 1: mostrar el video en la graphic interface
				#---TAREA 2: avanza 2 metros
				r.rpush("voiceEvents", json.dumps({'type': "voiceCommand", "name": "emergencia", "payload": {"edad": edad, "sexo": sexo}}, indent = 4))

				#AUDIO: Por favor, coloqua el dedo índice del paciente en mi sensor
				TTS1.Speak(Texto="Por favor, coloqua el dedo índice del paciente en mi sensor")

				#AUDIO: Sigue las instrucciones que se presentan en mi pantalla
				TTS1.Speak(Texto="Sigue las instrucciones que se presentan en mi pantalla")
				
				Success = True
			
			if Texto == "identificame":
				#identificar
				#EVENTO 1: abrir la camara
				#EVENTO 2: 
				pass
			
			if "chiste" in Texto:
				os.system("python Chistoso.py")
				Success = True

			if "curioso" in Texto:
				os.system("python Curioso.py")
				Success = True

			Intentos +=1

		r.rpush("vouceEvents", json.dumps({'type': "event", "name": "no-hearing"}, indent = 4))

main()