'''
	Este codigo realiza una busqueda en google de informacion y retorna el primer cuadro de texto
'''

import requests
import sys
from bs4 import BeautifulSoup
import Tex_Spe  as TS




#Esta funcion realiza busca en google y si encuentra un recuadro de recomnedacion lo reproduce en voz
def query(Peticion):
    
    URL = "https://www.google.co.in/search?q=" + Peticion

    #Buscar en google "show user agent y pegarlo en headers"
    headers = {
    	'User-Agent':'Mozilla/5.0 (X11; CrOS armv7l 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187 Safari/537.36'
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    answer = soup.find(class_="Z0LcW")
    
    return answer.get_text()

#Obtengo la oracion desde la linea de comando
consulta = sys.argv[1]
for i in range(len(sys.argv)-2): consulta = consulta + " " + sys.argv[2+i]


print("Astro puso en el buscador : ",consulta)


try:
	Texto = query(consulta)
except:
	Texto = "No he encontrado la respuesta"

TTS1 = TS.TTS()
TTS1.Speak(Texto)


