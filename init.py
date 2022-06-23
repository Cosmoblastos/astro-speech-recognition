'''
	Este codigo contiene el administrador de operaciones mediante comando de voz
'''

import os
import json
import time
from re import T
from tkinter import dialog
from lib.speech import STT, TTS
from lib.core import redis_db, global_config, dialogs


on = True #Este es el estao de astro
Tex_Spe = TTS()
Spe_Text = STT()


def voice_question (question: str, timeout: int = 4) -> str:
	if not question:
		raise RuntimeError("No question provided to voice_question")
	Tex_Spe.Speak(question)
	response = Spe_Text.listen(timeout)
	return response

def voice_event (event: str, data: any = None) -> None:
	if not event:
		raise RuntimeError("No event provided to publish_voice_event")
	redis_db.publish("voiceEvents", json.dumps({ "type": event, "payload": data }))


if __name__ == "__main__":
	#.................................................................................................................
	#Inicia el protocolo para escuchar a diestra y siniestra
	while on == True:

		#Instruccion para detectar el nombre del asistente
		STT.listen_keyword(global_config["activation_word"])

		#Escuchamos la instruccion
		print("\n\n I HERE YOU .................... \n\n")
		voice_event("listen")
		heard_command = Spe_Text.listen()
		print(f"\n\n HEARED COMMAND: {heard_command} \n\n")
		#TODO 1: add NLP to transform the heard_command into a specifitc and normalized command
		#TODO 2: validate that the command is valid

		attempts = 0
		success = False

		while attempts <3 and success == False:

			if heard_command == "hi":
				#VO: Hola, soy astro, tu asistente médico personal. ¿En que te puedo ayudar?
				Tex_Spe.Speak(dialogs.hi.d_1)
				Success = True

			if heard_command == "shutdown":
				voice_event("shutdown")
				on = False
				success = True

			if heard_command == "time":
				os.system("python ./lib/time.py")
				voice_event("time")
				success = True

			if heard_command == "communication":
				voice_event("show_webpage", "https://www.pictotraductor.com/")
				#VO: Abriendo herramienta de comunicación sin habla
				Tex_Spe.speak(dialogs.communication.d_1)
				success = True

			if "google" in heard_command:
				user_query = heard_command.replace("google","")
				print(user_query)
				voice_event("show_webpage", f"https://www.google.com/search?q={user_query}")
				os.system("python ./lib/google.py " + user_query)
				success = True

			if heard_command == "rehabilitation":
				#VO: "Acatzin, bienvenido a tu sesión de rehabilitación"
				Tex_Spe.speak(dialogs.rehabilitation.d_1)
				#VO: "¿Del 1 al 10 qué tan canssado te sientes hoy?"
				tired_level = voice_question(dialogs.rehabilitation.d_2)
				#VO: "¡De acuerdo! iniciemos"
				Tex_Spe.speak(dialogs.rehabilitation.d_3)
				voice_event("show_webpage", "https://www.youtube.com/embed/KmUVSXsHRic")
				success = True

			if heard_command == "emergency":
				#TODO: es necesario el saludo?
				#VO: Hola, soy astro, tu asistente médico personal
				Tex_Spe.Speak(dialogs.emergency.d_1)
				#VO: ¿Cuál es la emergencia?
				kind_of_emergency = voice_question(dialogs.emergency.d_2)
			
				if "heart" in kind_of_emergency and "attack" in kind_of_emergency:
					#VO: ¿Qué edad tiene la persona?
					age = voice_question(dialogs.emergency.d_3)
					#VO: ¿La persona es hombre o mujer?
					sex = voice_question(dialogs.emergency.d_4)

					#TODO: validar si es necesario esto
					#VO: "Coloca el dedo índice del paciente en mi sensor"
					Tex_Spe.Speak(dialogs.emergency.d_5)

					#TODO: convertir a RAIO para recivir las métricas
					voice_event("metrics")
					time.sleep(8)

					#TODO: eliminar el video del mapa
					#mostrar video de mapa
					voice_event("show_video", "mapa.mp4")
					#VO: "El paciente está teniendo un paro cardíaco, sus signos vitales se encuentran en mi pantalla y han sido enviados a los servicios de emergencia junto con tu ubicación"
					Tex_Spe.speak(dialogs.emergency.d_6)
					#mostrar video de emergencia
					voice_event("show_image", "rcp_img1.png")
					#VO: Por favor, colóquese a la altura del hombro del paciente con las rodillas estables en el suelo y con una ligera separación como se ve en mi imagen, comenzará a hacer compresiones
					Tex_Spe.speak(dialogs.emergency.d_7)
					voice_event("show_image", "rcp_img2.png")
					#VO: Las manos deben ir enlazadas con la palma de la mano dominante por debajo de la otra mano, para así poder apoyar el talón de la mano con mayor fuerza.
					Tex_Spe.Speak(dialogs.emergency.d_8)
					#VO: "Realizará 5 ciclos de 30 compresiones seguidas de 2 ventilaciones"
					Tex_Spe.Speak(dialogs.emergency.d_9)
					#VO: "Comprima de 5 a 7 centímetros en el pecho del paciente, justo en el lugar que se muestra, 30 veces al ritmo marcado"
					Tex_Spe.Speak(dialogs.emergency.d_10)
					#VO: "Listo, comenzamos"
					Tex_Spe.Speak(dialogs.emergency.d_11)
					voice_event("rcp_count")
					os.system("play compresion.mp3")

				else:
					#VO: "Lo siento, no tengo información sobre esa emergencia"
					Tex_Spe.speak(dialogs.emergency.d_7)
					success = True

				Success = True

			if "exercise" in heard_command:
				#VO: ¿Cuál es tu id?
				id = voice_question(dialogs.exercise.d_1)
				#VO: Muy bien, comenzaremos con 20 flexiones como las que se muestran en mi pantalla
				Tex_Spe.Speak(dialogs.exercise.d_2)
				voice_event("show_video", "ejercicio.mp4")
				#TODO: cmbiar a RAIO para saber cuando termina el video
				time.sleep(65) #duración del video de ejercicio
				#EVENTO: mostrar medidor de temperatura en pantalla de astro
				voice_event("temperature")
				#VO: Tu temperatura ahora es normal, por favor coloca tu dedo índice en mi sensor para revisar tus signos vitales
				Tex_Spe.Speak(dialogs.exercise.d_3)
				#TODO: cmbiar a RAIO para recibir las métricas
				voice_event("metrics")
				time.sleep(8)

				#VO: "Perfecto, vamos a comenzar, estaré revisando tus signos vitales constantemente."
				Tex_Spe.Speak(dialogs.exercise.d_4)
				voice_event("show_video", "dani_ejercicio.mp4")
				time.sleep(4)
				#VO: "¡Lo estas haciendo bien!"
				Tex_Spe.Speak(dialogs.exercise.d_5)

				success = True

			if "covid" in heard_command:
				#tomar temperatura
				voice_event("temperature")
				time.sleep(8)
				#VO: "Contesta las siguientes preguntas con un si o un no."
				Tex_Spe.Speak(dialogs.covid.d_1)
				#QUESTIONS:
				#VO: ¿Tienes tos?
				tos = voice_question(dialogs.covid.d_2)
				#VO: "¿Te cuesta respirar?"
				respirar = voice_question(dialogs.covid.d_3)
				#VO: "¿Has estado cerca de alguien que tiene coronavirus?"
				convivencia = voice_question(dialogs.covid.d_4)
				#VO: "¿Te duelen los músculos?"
				dolor = voice_question(dialogs.covid.d_5)
				#VO: "¿Has perdido el olfato y el gusto?"
				sentidos = voice_question(dialogs.covid.d_6)
				#VO: "¿Hace cuantos días te sientes así?"
				dias = voice_question(dialogs.covid.d_7)
				#TODO: calcular resultados
				#VO: Gozas de buena salud, sigue usando el cubrebocas, salva vidas
				Tex_Spe.Speak(dialogs.covid.d_8)
				success = True

			# if "emergency" in heard_command and "espacial" in heard_command:
			# 	Tex_Spe.Speak("Hola soy Astro tu asistente médico personal ¿Cual es el ID del paciente?")
			# 	id = voice_question("¿Cúal es el ID del paciente?")
			# 	Tex_Spe.Speak("Tengo sus datos. Coloca el dedo índice del paciente en mi sensor")
			# 	r.publish("voiceEvents", json.dumps({ "type": "metrics", "payload": True }))
			# 	Tex_Spe.Speak("El paciente está teniendo un paro cardíaco, sus signos vitales se encuentran en mi pantalla. Es hora de sujetarte a la estación, llevalo contigo")
			# 	Tex_Spe.Speak("Por favor colocate por detrás del paciente y coloca tus brazos alrededor del torso para ubicar tu mano dominante sobre la no dominante. Las manos deben ir al centro del tórax como se muestra en mi pantalla")
			# 	Success = True

			attempts += 1

