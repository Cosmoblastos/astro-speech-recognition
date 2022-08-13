from ast import parse
from lib.core import redis_db
import json
import time
from lib.speech import STT, TTS


Tex_Spe = TTS()
Spe_Text = STT()

def voice_question (question: str, timeout: int = 4) -> str:
	if not question:
		raise RuntimeError("No question provided to voice_question")
	Tex_Spe.speak(question)
	response = Spe_Text.listen(timeout)
	return response

def voice_event (event: str, data: any = None) -> None:
	if not event:
		raise RuntimeError("No event provided to publish_voice_event")
	redis_db.publish("voiceEvents", json.dumps({ "type": event, "payload": data }))


def performVoiceInstruction (instruction):
    data = None
    if 'waitForResponse' in instruction:
        if instruction['waitForResponse']:
            data = voice_question(instruction['say'])
    else:
        Tex_Spe.speak(instruction['say'])
    return data

def main ():
    pubsub = redis_db.pubsub()
    pubsub.subscribe(["voiceInstruction"])
    print("Listening for new messages in voiceInstruction channel")

    for message in pubsub.listen():
        print(message)
        if message['type'] == 'message':
            parsedMessage = json.loads(message['data'])
            if not "responseId" in parsedMessage:
                raise "No responseId provided"

            instruction = parsedMessage['instruction']
            data = performVoiceInstruction(instruction)

            responseId = parsedMessage["responseId"]
            responseChannel = f"voiceInstructionResponse:responseId={responseId}"
            redis_db.publish(responseChannel, json.dumps({
                "responseId": responseId,
                "success": True,
                "data": data
            }))


if __name__ == "__main__":
    main()
