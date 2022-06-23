from lib import VoiceCommand


class Emergency_VC (VoiceCommand):
    
    def __init__(self, keyword: str, dialogs: dict) -> None:
        super().__init__(keyword, dialogs)

    def execute (self):
        #TODO: es necesario el saludo?
        #VO: Hola, soy astro, tu asistente médico personal
        self.Tex_Spe.speak(self.dialogs.emergency.d_1)
        #VO: ¿Cuál es la emergencia?
        emergency_type = self.voice_question(self.dialogs.d_2)

        if "heart" in emergency_type and "attack" in emergency_type:
            self.heartAttack()

    def heartAttack (self):
        pass