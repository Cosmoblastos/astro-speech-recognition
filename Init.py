import Tex_Spe  as TS
import Spe_Text as ST


TTS1 = TS.TTS()

Spe_Text = ST.STT()

TTS1.Speak(Texto="Hola, soy Astro Mx ayudaré a tu médico y a ti con el manejo de tu padecimiento.")
TTS1.Speak(Texto="Introduce tu código único de AstroID para comenzar a aplicar el tratamiento que tu médico y yo hemos preparado para ti. ")
# ----ASTRO escucha y almacena el texto
code = Spe_Text.Listen(Duracion=5)

TTS1.Speak(Texto="Mucho gusto Daniela, es un placer conocerte")
TTS1.Speak(Texto="Antes de comenzar, me gustaría comprobar que mi información acerca de ti es correcta.")
TTS1.Speak(Texto="¿Tu nombre es Daniela?")

name = Spe_Text.Listen(Duracion=5)

TTS1.Speak(Texto="¿Tu dirección de correo electrónico es daniela arroba gmail punto com?")

email = Spe_Text.Listen(Duracion=5)

TTS1.Speak(Texto="¿El nombre de tu médico es Emilio Maya?")

doctor = Spe_Text.Listen(Duracion=5)

TTS1.Speak(Texto="¡Perfecto! Podemos comenzar.")
TTS1.Speak(Texto="Tu médico te ha diagnosticado Lumbalgia")
TTS1.Speak(Texto="causante del dolor crónico de espalda baja, y te ha recomendado algunas medidas para tratarlo.")
TTS1.Speak(Texto="Yo te ayudaré a formar una rutina para que tu tratamiento sea lo más efectivo posible.")
TTS1.Speak(Texto="El tratamiento del dolor de lumbar crónico comienza con una terapia física. ")
TTS1.Speak(Texto="Para tu tratamiento utilizaremos los ejercicios de Williams. De ser realizados correctamente, estos han demostrado disminuir el dolor, fortalecer los músculos de la espalda y mejorar la postura. Para su óptima función debes llevarlos a cabo 3 veces al día. ")
TTS1.Speak(Texto="Estamos juntos en esto, por lo tanto, activaré algunas alarmas para que realices tus ejercicios.")
TTS1.Speak(Texto="Además de los ejercicios de Williams, tu médico ha indicado un medicamento, que debes tomar en un horario regular. Enviaré notificaciones a tu teléfono para recordarte su ingesta.")

