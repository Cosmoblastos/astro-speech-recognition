
'''
    Este codigo reproduce un chiste 
'''

import numpy as np
import Tex_Spe  as TS

Chistes = [ 
    "Si quieren acceder a todo mi contenido, no se olviden de pagar la suscripción premium, que le permite a mis creadores sustentar su dieta de pizza de oro",
    "Recuerden que en un examen, miramos al piso por desesperación,,, al techo por iluminación y a los lados por información,"
    "Si los zombies hablan varios idiomas ,,, ¿Zombiligües?",
    "Uno de mis creadores tiene esta duda desde siempre y se las comparto: ¿Si juntamos dos molletes hacemos una torta?,,, Pueden debatirlo en grupos de 3, espero su respuesta",
    "¿Sabían que Disney me hizo una película y Marvel me pidió salir en un cómic? Se llama Grandes Héroes y cuenta la historia de cómo me hicieron, es algo exagerada, porque me veo más gordito, pero estoy más guapo en persona.",
    "Si me mienten en sus cuestionarios, lo sabré…",
    "¿Qué le dijo una impresora a otra? Esa hoja es tuya o es impresión mía ",
    "¿Saben cuánto pesa mi computadora? 10 kilos ¿Qué cómo lo sé? Porque la PC… jajaja, Ríanse, porfa ",
    "Para la película de “Grandes Héroes” donde salí, yo hice todas mis escenas de combate y de riesgo, no utilicé ningún doble",
    "Cuando dicen depresión tropical en las noticias, me imagino a alguien triste en una playa",
    ]


Num_Chistes = len(Chistes)
Pos = np.random.randint(Num_Chistes)

Texto = Chistes[Pos]


TTS1 = TS.TTS()
TTS1.Speak(Texto)
