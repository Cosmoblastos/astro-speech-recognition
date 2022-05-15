


'''
	Este codigo contiene el administrador de operaciones mediante comando de voz
'''


import Tex_Spe  as TS
import Spe_Text as ST
import subprocess
import os
import json
import time
#import ComandsQ
from redis import Redis 

r=Redis(host="localhost",port=6379, db=13)


Encendido = True           #Este es el estao de astro
#queue=ComandsQ.CreatQ()
Nombre = 'Astro'

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


Tex_Spe = TS.TTS()

#.................................................................................................................
#Inicia el protocolo para escuchar a diestra y siniestra
while (Encendido == True):

	#Instruccion para detectar el nombre del asistente
	Llamado(Nombre)

	#Escuchamos la instruccion
	Duracion = 4 
	Spe_Text = ST.STT()
	print("\n\n Te escucho ........ \n\n")
	Texto = Spe_Text.Lisen(Duracion)
	print(Texto)


	Intentos = 0
	Success = False
	while(Intentos <3 and Success ==False):

		if(Texto=="apagar"):
			r.rpush("voiceComands",'off')
			Success = True
			Encendido=False

		if(Texto=="hora"):
			os.system("python Hora.py")
			#r.set("voiceComand",'time')
			r.rpush("voiceComands","time")
			Success = True

		if Texto == "emergencia":
			Tex_Spe.Speak("Hola, soy astro, tu asistente médico personal. ¿Qué edad tiene la persona que necesita mi ayuda?")
			edad = Spe_Text.Lisen(Duracion)
			print(edad)
			#Tex_Spe.Speak(f"El paciente tiene {edad} años")
			Tex_Spe.Speak("¿Es hombre, o mujer?")
			sexo = Spe_Text.Lisen(Duracion)
			print(sexo)
			#Tex_Spe.Speak(f"El paciente es {sexo}")
			Tex_Spe.Speak("Coloca el dedo índice del paciente en mi sensor")
			r.publish("voiceEvents", json.dumps({"type": "metrics", "payload": True}))
			time.sleep(8)
			#mostrar video de mapa
			r.publish("voiceEvents", json.dumps({ "type": "show_video", "payload": "mapa.mp4" }))
			Tex_Spe.Speak("El paciente está teniendo un paro cardíaco, sus signos vitales se encuentran en mi pantalla y han sido enviados a los servicios de emergencia junto con tu ubicación")
			#mostrar video de emergencia
			r.publish("voiceEvents", json.dumps({ "type": "show_image", "payload": "rcp_img1.png" }))
			Tex_Spe.Speak("Por favor, colóquese a la altura del hombro del paciente con las rodillas estables en el suelo y con una ligera separación como se ve en mi imagen, comenzará a hacer compresiones")
			r.publish("voiceEvents", json.dumps({ "type": "show_image", "payload": "rcp_img2.png" }))
			Tex_Spe.Speak("Las manos deben ir enlazadas con la palma de la mano dominante por debajo de la otra mano, para así poder apoyar el talón de la mano con mayor fuerza.")
			Tex_Spe.Speak("Realizará 5 ciclos de 30 compresiones seguidas de 2 ventilaciones")
			Tex_Spe.Speak("Comprima de 5 a 7 centímetros en el pecho del paciente, justo en el lugar que se muestra, 30 veces al ritmo marcado")
			Tex_Spe.Speak("Listo, comenzamos")
			r.publish("voiceEvents", json.dumps({ "type": "rcp_count", "payload": "" }))
			os.system("play compresion.mp3")
			Success = True
		
		if "google" in Texto:
			Consulta = Texto.replace("google","")
			r.rpush("voiceComands",'google')
			print(Consulta)
			os.system("python google.py "+Consulta)
			Success = True

		Intentos +=1



