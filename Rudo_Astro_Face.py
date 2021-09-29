'''
	Este es el superpoderoso codigo de astro para el reconocimiento facial
		La idea es que este codigo contenga todo el script relacionado al reconocimiento facial

'''



import pickle 
import imutils
import os
import cv2
import numpy as np
import Tex_Spe  as TS

class AstroFace():

	#Metodo constructor
	def __init__(self):
		pass

		#Reviso si existe un archivo de Usuarios, de lo contrario lo creo
		try: 
			with open("Usuarios.pkl", "rb") as tf: self.Usuarios = pickle.load(tf)
		except: 
			self.Usuarios = {}
			with open("Usuarios.pkl", "wb") as tf: pickle.dump(self.Usuarios,tf)

		self.WorkDir = os.getcwd()           #Este es el directorio actual
		self.DataPath = self.WorkDir+"/Data/"            #Directorio donde se almacena la informacion de los usuarios
		self.ModelosPath = self.WorkDir+"/Modelos/"      #Directorio donde se almacenan los modelos de reconocimiento generados

		#Se actualizan los directorios por si cambia el dispositivo
		self.ActuDir()


	#Este metodo agrega un nuevo usuario
	def NewUsuario(self,Nombre):

		try:
			self.Usuarios[Nombre]
		except:
			Datos = {
					'label': len(self.Usuarios),
					'Path_Clip': self.DataPath+"Clips/"+Nombre+".mp4",
					'Path_Model': self.ModelosPath+Nombre+'.xml',
					'Path_Rostros': self.DataPath+Nombre+'/',
					'Contador': 0
			}

			self.Usuarios[Nombre]=Datos

		#Guardo la nueva informacion de los usuarios
		with open("Usuarios.pkl", "wb") as tf: pickle.dump(self.Usuarios,tf)

		print(self.Usuarios)

	#Este metodo actualiza los directorios de los usuarios
	def ActuDir(self):

		for Us in self.Usuarios:
			self.Usuarios[Us]['Path_Clip']     = self.DataPath+"Clips/"+Us+".mp4"
			self.Usuarios[Us]['Path_Model']    = self.ModelosPath+Us+'.xml'
			self.Usuarios[Us]['Path_Rostros']  = self.DataPath+Us


	#Este metodo obtiene las capturas de los rostros recortados desde un videoclip
	def MakeFaces(self,Nombre,Num):       

		#Se crea un directorio donde se guardaran los rostros capturados de las personas

		if not os.path.exists(self.Usuarios[Nombre]['Path_Rostros']):
			os.makedirs(self.Usuarios[Nombre]['Path_Rostros'])

		#Arbo el Clip con la informacion del usuario
		cap = cv2.VideoCapture(self.Usuarios[Nombre]['Path_Clip'])
		faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

		#Abro el video lo redimenciono y substraigo Num capturas del rostro       
		count = 0      
		while True:

			#Obtengo los frame
			ret, frame = cap.read()              ####Computadora             
			#frame = self.capture_frame()        ####Raspberry
			
			#Reviso si se encontro el video
			if (ret == False):
				print("No se encontro el video")
				break

			#Redimenciono la imagen
			frame =  imutils.resize(frame, width=640)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			auxFrame = frame.copy()

			faces = faceClassif.detectMultiScale(gray,1.3,5)

			for (x,y,w,h) in faces:
				cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
				rostro = auxFrame[y:y+h,x:x+w]
				rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
				cv2.imwrite(self.Usuarios[Nombre]['Path_Rostros']+ '/rostro_{}.jpg'.format(count),rostro)
				count = count + 1

			#Esta instruccion permite visualizar el entrenamiento 
			cv2.imshow('frame',frame)

			k =  cv2.waitKey(1)
			if k == 27 or count >= Num:
				break
		cap.release()
		cv2.destroyAllWindows() 

	#Este metodo entrena un modelo particular para un solo usuario usando todas las imagenes
	def GetModel_Individual(self,Nombre):

		#Obtengo las direcciones de todas las imagenes de entrenamiento pertenecientes a Nombre
		facesData = []        
		for fileName in os.listdir(self.Usuarios[Nombre]['Path_Rostros']):
			facesData.append(cv2.imread(self.Usuarios[Nombre]['Path_Rostros']+'/'+fileName,0))

		#Se entrenara el modelo para que retorne 0 cuando reconosca el rostro
		labels = [self.Usuarios[Nombre]['label'] for i in range(len(facesData))]

		# Se crea el modelo, se entrena y se guarda
		face_recognizer = cv2.face.LBPHFaceRecognizer_create()
		face_recognizer.train(facesData, np.array(labels))
		face_recognizer.write(self.Usuarios[Nombre]['Path_Model'])
		#face_recognizer.write('./Modelos/Modelo_'+Nombre+'.xml')

	#Este metodo entrena un modelo para todos los usuarios
	def GetModel_Group(self):

		Rostros = []
		Etiquetas = []

		#Para todos los usuarios
		for Use in self.Usuarios:

			#Para todas los rostros que tiene el usuario
			for fileName in os.listdir(self.Usuarios[Use]['Path_Rostros']):
				Etiquetas.append(self.Usuarios[Use]['label'])
				Rostros.append(cv2.imread(self.Usuarios[Use]['Path_Rostros']+'/'+fileName,0))

		# Se crea el modelo y se entrena
		face_recognizer = cv2.face.LBPHFaceRecognizer_create()
		# Entrenando el reconocedor de rostros
		face_recognizer.train(Rostros, np.array(Etiquetas))

		# Almacenando el modelo obtenido
		face_recognizer.write(self.ModelosPath+'Usuarios.xml')


	#Este metodo utilizara Num capturas de rostro para identificar al usuario utilizando el modelo entrenado con todos los usuarios
	def Identificar(self,Num):

		#Identifico los usuarios del astro local y creo un contador para contar las veces que reconoce a cada usuario
		Nombres = self.Usuarios.keys()
		Names = []
		for Nom in Nombres:	Names.append(Nom)

		#Abro la camara y codigo para reconocer rostros
		webcam = cv2.VideoCapture(0)
		faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')     #Compu
		#faceClassif = cv2.CascadeClassifier('/home/pi/Desktop/Cosmoblastos/Practicas/practicas-server/haarcascade_frontalface_default.xml')       #Astro

		#Abro el modelelo de reconocimiento que se utilizara
		face_recognizer = cv2.face.LBPHFaceRecognizer_create()
		face_recognizer.read(self.ModelosPath+'Usuarios.xml')

		#Abro el bucle para tomar los frames y los rostros de la persona
		chek= 0
		while(chek<Num):
			chek+=1

			#Obtengo un frame de la camara
			(_,frame) = webcam.read()                #Compu
			#frame = self.capture_frame()            #Rasp

			#Acondiciono el frame
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			auxFrame = gray.copy()
			faces = faceClassif.detectMultiScale(gray,1.1,5)

			#print(faces)
			for (x,y,w,h) in faces:
				rostro = auxFrame[y:y+h,x:x+w]
				rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
				result = face_recognizer.predict(rostro)

				cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)

				# LBPHFace
				if result[1] < 80:
					cv2.putText(frame,'{}'.format(Names[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
				else:
					cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)


			#Esta instruccion permite visualizar el entrenamiento 
			cv2.imshow('frame',frame)

			k =  cv2.waitKey(1)
			if k == 27 or chek >= Num:
				break
		webcam.release()
		cv2.destroyAllWindows() 

	#Este metodo utilizara Num capturas de rostro para identificar al usuario utilizando el modelo entrenado con todos los usuarios
	def Reconocer(self,Num):

		#Abro la camara y codigo para reconocer rostros
		webcam = cv2.VideoCapture(0)
		faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')     #Compu
		#faceClassif = cv2.CascadeClassifier('/home/pi/Desktop/Cosmoblastos/Practicas/practicas-server/haarcascade_frontalface_default.xml')       #Astro

		Modelos = []
		for Us in self.Usuarios:
			face_recognizer = cv2.face.LBPHFaceRecognizer_create()
			face_recognizer.read(self.Usuarios[Us]['Path_Model'])
			Modelos.append(face_recognizer)	
			self.Usuarios[Us]['Contador'] = 0	

		#Identifico los usuarios del astro local y creo un contador para contar las veces que reconoce a cada usuario
		Nombres = self.Usuarios.keys()
		Names = []
		for Nom in Nombres: Names.append(Nom)
		Contador= np.zeros(len(Names))

		#Abro el bucle para tomar los frames y los rostros de la persona
		chek= 0
		while(chek<Num):
			chek+=1

			#Obtengo un frame de la camara
			(_,frame) = webcam.read()                #Compu
			#frame = self.capture_frame()            #Rasp

			#Acondiciono el frame
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			auxFrame = gray.copy()
			faces = faceClassif.detectMultiScale(gray,1.1,5)

			for (x,y,w,h) in faces:
				rostro = auxFrame[y:y+h,x:x+w]
				rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)

				for i in range(len(Modelos)):
					result = Modelos[i].predict(rostro)
					if(result[0]==i and result[1]<90): Contador[i] = Contador[i] + 1


				cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)

				# LBPHFace
				if result[1] < 75:
					#cv2.putText(frame,'{}'.format(Names[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
				else:
					#cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
					cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)


			#Esta instruccion permite visualizar el entrenamiento 
			cv2.imshow('frame',frame)

			k =  cv2.waitKey(1)
			if k == 27 or chek >= Num:
				break
		webcam.release()
		cv2.destroyAllWindows() 

		TTS1 = TS.TTS()
		if(max(Contador)<0.5*Num):
			Usuario = "Desconocido"
			TTS1.Speak("No te he reconocido, intenta mirar fijamente a la camara")
		else:
			NumUser = np.where(Contador==max(Contador))[0][0]
			Usuario = Names[NumUser]
			TTS1.Speak("Reconosco a "+Usuario) 
			print(Usuario)
			print(Contador)








#......................................................................................................
Prueba = AstroFace()

#Name = "Alejandro"
#Name = "Zapett"
#Name = "DaniV"
#Name = "DaniG"
#Name = "Acatzin"
#Name = "Kary"


#Prueba.NewUsuario(Name)                 #Nombre del nuevo usuario#
#Prueba.MakeFaces(Name,50)               #Nombre del usuario y numero de capturas del rostro solicitadas
#Prueba.GetModel_Individual(Name)        #Obtener el modelo particular para un usuario
#Prueba.GetModel_Group()                 #Obtener el modelo para todos los usuarios
Prueba.Identificar(100)       #Numero de frames para reconoces
#Prueba.Reconocer(50)           #Numero de frames para identificar





