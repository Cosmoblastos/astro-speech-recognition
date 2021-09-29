import redis
import Tex_Spe  as TS

TTS1 = TS.TTS()

publisher = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
pubsub = publisher.pubsub()

pubsub.subscribe("faceIdentification")

for message in pubsub.listen():
	print("Redis: ")
	print(message)
	if (message['channel'] == 'faceIdentification'):
        print("Eres "+ message['data'])
	    Speaker("Eres "+ message['data'])
        # speak message['data']

def Speaker(Texto):
    TTS1.Speak(Texto)