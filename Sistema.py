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

# Configuración inicial
r=Redis(host="localhost",port=6379)

Encendido = True

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

def main():
    TTS1 = TS.TTS()
    
    while(Encendido):
        #Detección del nombre del asistente:
        Llamado(Nombre)
        #Nueva instrudcción
	Duracion = 3
	Spe_Text = ST.STT()
        print("\n\n Te escucho .... \n\n")
	r.publish("voiceDetected", "astro");
	#r.rpush("voiceEvents", json.dumps({'type': "event", "name": "hearing"}, indent = 4))
	Texto = Spe_Text.listen(Duracion)
	print(Texto)

	if not Texto continue

	Intentos = 0
	Exito = False
	while(Intentos < 3 and Exito == False):
			
	    if "hora" in  Texto:
	        os.system("python3 Hora.py")
		Existo = True

	    if (Texto == "presentate" or Texto == "preséntate"):
		#TODO: abstraer funcionalidad de audio
		TTS1.Speak(Texto="Hola, soy ASTRO, tu asistente médico personal")
		Exito = True

	    if "google" in Texto:
		Consulta = Texto.replace("google","")
		os.system("python3 google.py " + Consulta)
		Exito = True

	    if "chiste" in Texto:
		os.system("python3 Chistoso.py")
		Exito = True

	    if "curioso" in Texto:
		os.system("python3 Curioso.py")
		Exito = True

	    if ("quién soy" in Texto or "quien soy" in Texto):
    		r.publish("faceRecognition", "quien soy")
		Exito = True

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
		#r.rpush("voiceEvents", json.dumps({'type': "voiceCommand", "name": "emergencia", "payload": {"edad": edad, "sexo": sexo}}, indent = 4))

		#AUDIO: Por favor, coloqua el dedo índice del paciente en mi sensor
		TTS1.Speak(Texto="Por favor, coloqua el dedo índice del paciente en mi sensor")

		#AUDIO: Sigue las instrucciones que se presentan en mi pantalla
		TTS1.Speak(Texto="Sigue las instrucciones que se presentan en mi pantalla")
				
		Exito = True

	    if(Exito == False):
		if(Intentos < 2):
		    TTS1.Speak(Texto="No te entendí, ¿Puedes repetirlo?")
		else: 
		    TTS1.Speak(Texto="Lo lamento, no te entendí")

	    Intentos +=1

if __name__ == "__main__":
    main()



