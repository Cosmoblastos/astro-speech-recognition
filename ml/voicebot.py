import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import pickle
from nltk.stem import SnowballStemmer
from nltk import tokenize

# Creamos una clase que contendra el chatbot
class ChatAstro():

    # Metodo constructor
    def __init__(self):

        # Abrimos el diccionario con las respuestas
        with open("Respuestas.pkl", "rb") as tf: self.Response = pickle.load(tf)

        # Abrimos el diccionario con las respuestas
        with open("Palabras.pkl", "rb") as tf: self.Palabras = pickle.load(tf)
        
        # Listamos las intenciones 
        self.Intenciones = list(self.Response.keys())

        #Cargo el modelo de Catboost
        self.Modelo = CatBoostRegressor()
        self.Modelo.load_model('./CatB_ChAstro.model')

    
    # Metodo conversar
    def Conversar(self,Texto):

        # Transformamos el texto para poder procesarlo
        spanish_stemmer = SnowballStemmer('spanish')
        Prue_Tok = tokenize.word_tokenize(Texto,preserve_line=True)          # Tokenizamos la palabra
        Prue_Lem = [ spanish_stemmer.stem(wor.lower()) for wor in Prue_Tok if not wor in ['!','?','¿','.',',','*','+','-','/']]   # Lematizamos y quitamos simbolos
        Prue_Vec = np.zeros(len(self.Palabras))
        for i in range(len(self.Palabras)):
            if( self.Palabras[i] in Prue_Lem): Prue_Vec[i] = 1 

        # Identifico la intencion y regreso una respuesta aleatoria
        Pred = self.Modelo.predict(Prue_Vec)
        Pos = np.where(Pred == np.max(Pred))[0][0]
        
        Intent = self.Intenciones[Pos]
        Res = np.random.permutation(len(self.Response[Intent]))[0]
        Res = self.Response[Intent][Res]

        return Res



if __name__ == "__main__":
    # Se crea el objeto y 
    Perico = ChatAstro()
    Texto = 'Hi, how are you?'
    print(Perico.Conversar(Texto))

    Texto = 'Could you tell me a joke?'
    print(Perico.Conversar(Texto))

    Texto = 'Who am I?'
    print(Perico.Conversar(Texto))

    Texto = 'Turn off'
    print(Perico.Conversar(Texto))

    Texto = 'What time is it?'
    print(Perico.Conversar(Texto))
