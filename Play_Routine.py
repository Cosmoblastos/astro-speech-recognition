
import Tex_Spe  as TS
import Spe_Text as ST


TTS1 = TS.TTS()

Spe_Text = ST.STT()

TTS1.Speak(Texto="A continuación te mostraremos el procedimiento que debes seguir. ")
# ----ASTRO escucha y almacena el texto

code = Spe_Text.Listen(Duracion=5)

TTS1.Speak(Texto="Ejercicio uno. Acostado boca arriba, con una pierna flexionada, eleve la otra rodilla, recta. La cuenta inicia cuando sube el pie, realizarlo con ambas piernas.")
TTS1.Speak(Texto="Ejercicio dos. Acostado boca arriba con las piernas flexionadas, llevarlas hacia el pecho ayudadas con las manos y retomar a su posición inicial. Mantener la espalda pegada al piso en todo momento.")
TTS1.Speak(Texto="Ejercicio tres. Acostado boca arriba, flexiona la cadera y la rodilla a noventa grados y comienza a hacer movimientos circulares en ambos sentidos. Giro hacia un lado y hacia el otro para terminar primera repetición. ")
TTS1.Speak(Texto="Ejercicio cuatro. Acostado boca arriba, con las piernas flexionadas, realice abdominales con los brazos en el pecho")
TTS1.Speak(Texto="Ejercicio cinco. Acostado boca arriba con las rodillas flexionadas levanta los glúteos despegándose de la cama, contar hasta 5 y descender")
TTS1.Speak(Texto="Ejercicio seis. Arrodíllate sobre el piso, apoyando las palmas de la mano, debe arquear exageradamente la espalda, aumentando la flexión del tronco. ")
TTS1.Speak(Texto="Mantener cada posición durante cinco segundos y reposar cinco segundos y vuelva a la posición de partida.")
TTS1.Speak(Texto="Repeticiones: cinco repeticiones, una serie.")
TTS1.Speak(Texto="Series: dos series  Frecuencia : tres  veces por semana. Duración :Indefinido")




