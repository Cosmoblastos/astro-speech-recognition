


'''
	Este codigo contiene el administrador de operaciones mediante comando de voz
'''


from re import T
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


def voice_question (question):
	if not question:
		raise RuntimeError("No question provided to voice_question")
	Tex_Spe.Speak(question)
	response = Spe_Text.Lisen()
	return response

#.................................................................................................................
#Inicia el protocolo para escuchar a diestra y siniestra
while (Encendido == True):

	#Instruccion para detectar el nombre del asistente
	Llamado(Nombre)

	#Escuchamos la instruccion
	Duracion = 4 
	Spe_Text = ST.STT()
	print("\n\n Te escucho ........ \n\n")
	r.publish("voiceEvents", json.dumps({ "type": "listen", "payload": True }))
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

		if Texto == "inicio":
			Tex_Spe.Speak("Hola, soy astro, tu asistente médico personal. ¿En que te puedo ayudar?")
			Success = True

		if "ejercicio" in Texto:
			Tex_Spe.Speak("¿Cúal es tu ID?")
			id = Spe_Text.Lisen()
			print(id)
			Tex_Spe.Speak("Muy bien, comenzaremos con 20 flexiones como las que se muestran en mi pantalla")
			r.publish("voiceEvents", json.dumps({ "type": "show_video", "payload": "ejercicio.mp4" }))
			time.sleep(65) #duración del video de ejercicio

			r.publish("voiceEvents", json.dumps({"type": "temperature", "payload": True}))
			
			#EVENTO: mostrar medidor de temperatura en pantalla de astro
			Tex_Spe.Speak("Tu temperatura ahora es normal, por favor coloca tu dedo índice en mi sensor para revisar tus signos vitales")
			r.publish("voiceEvents", json.dumps({"type": "metrics", "payload": True}))
			time.sleep(8)

			Tex_Spe.Speak("Perfecto, vamos a comenzar, estaré revisando tus signos vitales constantemente.")
			r.publish("voiceEvents", json.dumps({"type": "show_video", "payload": "dani_ejercicio.mp4"}))
			
			time.sleep(4)
			Tex_Spe.Speak("¡Lo estas haciendo bien!")

			Success = True

		if "covid" in Texto:
			#tomar temperatura
			r.publish("voiceEvents", json.dumps({ "type": "temperature", "payload": True }))
			time.sleep(8)
			Tex_Spe.Speak("Contesta las siguientes preguntas con un si o un no.")
		
			tos = voice_question("¿Tienes tos?")
			respirar = voice_question("¿Te cuesta respirar?")
			convivencia = voice_question("¿Has estado cerca de alguien que tiene coronavirus?")
			dolor = voice_question("¿Te duelen los músculos?")
			sentidos = voice_question("¿Has perdido el olfato y el gusto?")
			dias = voice_question("Para finalizar, ¿Puedes decirme hace cuantos días te sientes así?")
			#TODO: calcular resultados
			
			Tex_Spe.Speak("Gozas de buena salid, sigue usando el cubrebocas, salva vidas.")
			Success = True

		if "emergencia" in Texto and "espacial" in Texto:
			Tex_Spe.Speak("Hola soy Astro tu asistente médico personal ¿Cual es el ID del paciente?")
			id = voice_question("¿Cúal es el ID del paciente?")
			Tex_Spe.Speak("Tengo sus datos. Coloca el dedo índice del paciente en mi sensor")
			r.publish("voiceEvents", json.dumps({ "type": "metrics", "payload": True }))
			Tex_Spe.Speak("El paciente está teniendo un paro cardíaco, sus signos vitales se encuentran en mi pantalla. Es hora de sujetarte a la estación, llevalo contigo")
			Tex_Spe.Speak("Por favor colocate por detrás del paciente y coloca tus brazos alrededor del torso para ubicar tu mano dominante sobre la no dominante. Las manos deben ir al centro del tórax como se muestra en mi pantalla")
			Success = True

		if "google" in Texto:
			Consulta = Texto.replace("google","")
			r.rpush("voiceComands",'google')
			print(Consulta)
			os.system("python google.py "+Consulta)
			Success = True

		Intentos +=1



