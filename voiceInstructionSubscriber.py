from ast import parse
from lib.core import redis_db
import json
import time
from lib.speech import STT, TTS
from lib.core import global_config


Tex_Spe = TTS(lang=global_config['output_lang'])
Spe_Text = STT(lang=global_config['input_lang'])

def voice_question (question: str, timeout: int = 4) -> str:
	if not question:
		raise RuntimeError("No question provided to voice_question")
	Tex_Spe.speak(question)
	response = Spe_Text.listen(timeout)
	return response

def performVoiceInstruction (instruction):
    if 'response' in instruction:
        if instruction['response']['waitFor']:
            dataValue = voice_question(instruction['say'])
            return {
                "name": instruction['response']['expectedValueName'], 
                "type": instruction['response']['expectedType'],
                "value": dataValue
            }
    else:
        Tex_Spe.speak(instruction['say'])

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
