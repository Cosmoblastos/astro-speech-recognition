from lib import VoiceCommand

class Exercise_VC (VoiceCommand):

    def __init__(self, keyword: str, dialogs: dict) -> None:
        super().__init__(keyword, dialogs)
    
    # método estándar para definición del flujo principal del comando.
    def execute (self):
        # Debe recibir un ID del ejercicio
        try:
            selectedExercise = self.welcome()
            exercise = self.get_exercise(selectedExercise)
            self.Spe_Text.speak(f"Mostrando ejercicio {exercise.name}")
            self.voice_event("show_video", exercise.url)
        except Exception as e:
            self.voice_event("error", { "message": "No existe el ejercicio seleccionado" })
            print(e)
            #self.error(e)


    def welcome (self):
        self.Tex_Spe.speak("Hola, Fernando")
        selectedExercise = self.voice_question("¿Qué ejercicio deseas realizar?", 4)
        return selectedExercise

    def get_exercise (self, selectedExercise):
        # 1: utilizar el método de VoiceComamnd para consultar la DB con el nombre del ejercicio
        # 2: retornar el ejercicio
        # 3: si no retorna nada la DB, realizar una excepción
        pass