import pandas as pd
import numpy as np

#  Abrimos el documento con las conducata realizada
Conducta = pd.read_csv("../assets/Conducta_En.csv")

# Filtramos las acciones con las que se identifica la intencion
Acciones = Conducta[Conducta['Movimiento']=='Accion']

# ................. Preprocesamos la informacion ..........................................
Oraciones = Acciones['Contenido'].values    #Se acceden a todos los contenidos registrados

# Identificamos todas las palabras que contiene nuestro conjunto de acciones
from nltk import tokenize

# Tokenizamos las oraciones
Ora_Token = []  
for ora in Oraciones: Ora_Token.append(tokenize.word_tokenize(ora,preserve_line=True))

# Quitamos simbolos, hacemos en minuscula y lematizamos la informacion (reducir las palabra a su expresion mas simple)
from nltk.stem import SnowballStemmer
spanish_stemmer = SnowballStemmer('english')

Ora_Lema = []
for Ora in Ora_Token:
    New= []
    for pal in Ora:
        if not pal in ['!','?','¿','.',',','*','+','-','/']: 
            New.append(spanish_stemmer.stem(pal.lower()))
    Ora_Lema.append(New)

# ................. Codificamos la informacion ............................................

# Hacemos una lista sin repeticion de todas las palabras que contiene el set de entrenamiento
Palabras = []
for Ora in Ora_Lema:
    for pal in Ora:
        if not pal in Palabras: Palabras.append(pal)
Palabras = np.array(Palabras)

# Codificamos cada una de las oraciones con base en su contenido en las palabras
Ora_Vec = np.zeros((len(Ora_Lema),len(Palabras)))

for pos_pal in range(len(Palabras)):
    for pos_ora in range(len(Ora_Lema)):
        if Palabras[pos_pal] in Ora_Lema[pos_ora]: Ora_Vec[pos_ora][pos_pal] = 1

# ................ Construimoslas etiquetas para el entrenamiento

# Definimos las etiquetas para el conjunto de entrenamiento

Intenciones = []
for item in Acciones['Intencion']: 
    if not (item in Intenciones): Intenciones.append(item)

Etiquetas = np.zeros((len(Ora_Vec),len(Intenciones)))
List_Actions = Acciones['Intencion'].values
for i in range(len(List_Actions)): 
    pos = Intenciones.index(List_Actions[i])
    Etiquetas[i][pos]=1

#.....................  Entrenamos el modelo y lo guardamos .............................

#Utilizo Catboost regresor
#https://coderzcolumn.com/tutorials/machine-learning/catboost-an-in-depth-guide-python#5
from catboost import CatBoostRegressor

CatB = CatBoostRegressor(
                        iterations = 500,
                        #max_depth = 8,
                        verbose=False,     #Cada cuando se imprimen resultados   
                        random_seed=1000,
                        loss_function = 'MultiRMSE',
                        )

CatB.fit(Ora_Vec,Etiquetas)

#Guardamos el modelo
CatB.save_model(fname =  './CatB_ChAstro.model')

# ..................... Generamos un diccionario con las posibles respuestas ........

import pickle

# Hacemos un diccionario con las respuestas posibles para cada accion
Reaccion = Conducta[Conducta['Movimiento']=='Reaccion']

# Guardamos una lista con las respuestas posibles del Chatboot
Respuestas = {}
for int in Intenciones:
    Aux = Reaccion[Reaccion['Intencion'] == int]
    Respuestas[int] = list(Aux['Contenido'])

with open("Respuestas.pkl", "wb") as tf:
    pickle.dump(Respuestas,tf)

with open("Palabras.pkl", "wb") as tf:
    pickle.dump(Palabras,tf)

#print(Palabras)

print("............ENTRENADO y GUARDADO ...................")

