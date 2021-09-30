import redis
import Tex_Spe  as TS

TTS1 = TS.TTS()

publisher = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
pubsub = publisher.pubsub()

def speaker(Texto):
    TTS1.Speak(Texto)

pubsub.subscribe("faceIdentification")

for message in pubsub.listen():
    print("Redis: ")
    print(message)
    if (message['channel'] == 'faceIdentification'):
        if(isinstance(message['data'], str)):
            print("Eres "+ str(message['data']))
            speaker("Eres "+ str(message['data']))
