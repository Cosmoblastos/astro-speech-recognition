'''
	Este codigo escucha en periodos de 1 segundo para identificar una palabra clave
'''

import speech
import sys
from core import global_config


#Esta funcion revisa el microfono hasta escuchar el nombre
def pay_attention (keyword: str) -> None:
	heard_text = ""
	duration = 1 #Segundos de revicion
	Spe_Text = speech.STT()

	while keyword != heard_text:
		#Esperamos la instruccion de invocacion con el Nombre del asistente
		heard_text = Spe_Text.listen(duration)


if __name__ == "__main__":
	arg_keyword = sys.argv[1]
	keyword = arg_keyword or global_config["activation_word"]
	pay_attention(keyword)