'''

	Este codigo escucha en periodos de 1 segundo para identificar una palabra clave

'''

import Spe_Text as ST

#Palabra clave que se quiere identificar
Nombre     = "astro"         

#Esta funcion revisa el microfono hasta escuchar el nombre
def Llamado(Keyword):
	Texto = False
	Spe_Text = ST.STT()

	while (Keyword!=Texto):

		#Esperamos la instruccion de invocacion con el Nombre del asistente
		Duracion = 1                      #Segundos de revicion

		Texto = Spe_Text.Lisen(Duracion)



Llamado(Nombre)