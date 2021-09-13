
import gtts
import os

#Esta clase realiza el "text_to_speech"
class TTS():

	#Inicializo el paquete y lo defino en espanol
	def __init__(self):
		pass

	#Convierto el texto en audio y lo reproduzco
	def Speak(self,Texto):

		tts = gtts.gTTS(Texto,lang = "es-us")
		tts.save("Audio.mp3")
		os.system('play Audio.mp3')

'''
Texto = "Tu sonrisa tan resplandeciente,,, A mi corazon deja encantado ,,, Ven toma mi mano,,, Para huir de esta terrible oscuridad"

TTS1 = TTS()
TTS1.Speak(Texto)
'''