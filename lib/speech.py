import speech_recognition as sr
import gtts
import os
import time
import subprocess

#Calse speech to text
'''
	Este codigo utiliza el microfono de la rasp y convierte el Speech to text
'''
class STT:

	#Inicializo el paquete
	def __init__(self):
		self.chismoso = sr.Recognizer()

	#Utilzo el paquete para escuchar y convertir el audio en texto
	def listen(self, duration: int = 5) -> str:

		#print("Escuchando ...")
		with sr.Microphone() as source:

			audio = self.chismoso.listen(source, phrase_time_limit=duration)
			texto = False

			try:
				text = self.chismoso.recognize_google(audio, language="en-US")
				texto = text.lower()
			except Exception as e:
				print(f"----------- Speech To Text Error -----------: {e}")

		return texto

	#Esta funcion utiliza 35 subprocesos para identificar si se ha mencionando el nombre del asistente 
	def listen_keyword(self, keyword: str):

		script_path = os.path.join(os.getcwd(), "lib/listen.py")

		child0 = subprocess.Popen(['python', script_path, keyword])
		time.sleep(0.2)
		child1 = subprocess.Popen(['python', script_path, keyword])
		time.sleep(0.2)
		child2 = subprocess.Popen(['python', script_path, keyword])
		time.sleep(0.2)
		child3 = subprocess.Popen(['python', script_path, keyword])
		time.sleep(0.2)
		child4 = subprocess.Popen(['python', script_path, keyword])

		while (
			child0.poll() == None and 
			child1.poll() == None and 
			child2.poll() == None and 
			child3.poll() == None and 
			child4.poll() == None
		): 
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

	


#Esta clase realiza el "text_to_speech"
class TTS:

	#Inicializo el paquete
	def __init__(self):
		pass

	#Convierto el texto en audio y lo reproduzco
	def speak(self, message: str) -> None:
		tts = gtts.gTTS(message)
		tmpAudioPath = os.path.join(os.getcwd(), "audio/tmp_audio.mp3")
		tts.save(tmpAudioPath)
		os.system(f'play {tmpAudioPath}')


if __name__ == "__main__":
	stt = TTS()
	stt.speak("Hello, I'm Astro")
