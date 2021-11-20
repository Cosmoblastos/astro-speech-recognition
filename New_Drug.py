import Tex_Spe  as TS
import Spe_Text as ST


TTS1 = TS.TTS()

Spe_Text = ST.STT()

TTS1.Speak(Texto="¿Qué medicamento vas tomar?")

drug = Spe_Text.Listen(Duracion=5)

TTS1.Speak(Texto="Estableceré alarmas usando tu nuevo horario")