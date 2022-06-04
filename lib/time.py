'''
	Este codigo reproduce la hora actual
'''

from datetime import datetime
import speech


#Obtengo la informacion de la hora
now = datetime.now()

#Identifico la hora y minutos
hora = now.hour
minutos = now.minute

print(str(hora))

if hora == 1:
	texto = "Es la una con "+ str(minutos) + " minutos"
else:
	texto = "Son las " +str(hora) + "con " + str(minutos) +  "minutos" 



TTS1 = speech.TTS()
TTS1.speak(texto)
