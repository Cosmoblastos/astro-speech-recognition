import json
from core import redis_db
from speech import STT, TTS


class VoiceCommand:

    def __init__(self, keyword: str, dialogs: dict):
        self.keyword = keyword
        self.dialogs = dialogs
        self.Tex_Spe = TTS()
        self.Spe_Text = STT()

    def voice_question (self, question: str, timeout: int = 4) -> str:
        if not question:
            raise RuntimeError("No question provided to voice_question")
        self.Tex_Spe.speak(question)
        response = self.Spe_Text.listen(timeout)
        return response

    def voice_event (self, event: str, data: any = None) -> bool:
        if not event:
            raise RuntimeError("No event provided to publish_voice_event")
        redis_db.publish("voiceEvents", json.dumps({ "type": event, "payload": data }))
        return True
    