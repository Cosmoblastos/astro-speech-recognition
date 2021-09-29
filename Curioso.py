

'''
    Este codigo reproduce un chiste 
'''

import numpy as np
import Tex_Spe  as TS

Datos = [ 

    "El hueso temporal se llama así, porque es el “hueso del tiempo”, ya que ahí es donde se ven las primeras canas.",
    "Una de las proteínas del ojo se llama “Pikachurina”, la cual es una proteína que permite convertir estímulos luminosos en eléctricos y sí, tiene inspiración en Pikachú.",
    "Otro personaje de los videojuegos en la Medicina es Sonic el erizo, pues un gen muy importante para el desarrollo del embrión tiene su nombre Sonic Hedgehog",
    "La mayoría de los huesos del cuerpo humano se encuentran en las manos y los pies, teniendo 27 y 26 huesos respectivamente, dando un total de 54 y 52 huesos por ambas manos, pero si los juntamos, nos dan 106 huesos de los 206 que tiene un adulto.",
    "El hueso sacro, es “el hueso sagrado” porque cuando alguien en la Edad Media era acusado de brujería y llevado a la hoguera, era uno de los huesos que no se quemaba, además por su forma muy similar a la de un corazón, les hizo creer los Inquisidores que era señal de que se habían purificado y por lo tanto, era sagrado.",
    "Realmente sí usamos el 100% de nuestro cerebro, no hay área que no se use e incluso, existen “mapas para el cerebro” que lo dividen en áreas de acuerdo con su función, siendo el más famoso el de Brodmann con aproximadamente 47 áreas.",
    "¿Les gustan los idiomas? Pues resulta que las personas que hablan más de un idioma tienen menos probabilidades de padecer Alzheimer y tienen un mayor umbral para desarrollar una crisis epiléptica, así que ya saben, aprendan un nuevo idioma ",
    "¿Sabían que hay un músculo que no todo el mundo tiene? Se llama palmar largo y su tendón es visible cuando juntamos el dedo pulgar y el meñique, pero no todos lo poseen, pues es un vestigio evolutivo.",
    "Los niños recién nacidos tienen un reflejo que se llama “de prensión” y esto es otro vestigio evolutivo, pues los bebés de los primeros primates al nacer debían agarrarse de la espalda de la mama para no caerse y este reflejo se conserva en la mayoría de los primates actuales, incluidos los seres humanos",
    "Tenemos una relación muy íntima con las bacterias y algunos tipos de hongos, los cuales recubren nuestro cuerpo y algunas cavidades. Estos nos ayudan a no enfermarnos y a mantener lejos a otros microorganismos peligrosos, a todo este conjunto de seres microscópicos los llamamos “microbiota”"
    ]


Num_Datos = len(Datos)
Pos = np.random.randint(Num_Datos)

Texto = Datos[Pos]



TTS1 = TS.TTS()
TTS1.Speak(Texto)
