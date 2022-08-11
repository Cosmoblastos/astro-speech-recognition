from lib.core import redis_db

def main():
    pubsub = redis_db.pubsub()
    pubsub.subscribe(['ui_io'])
    print('Listening for new messages')
    for message in pubsub.listen():
        #TODO:
        #parse message to json
        #get action, if is a question use the voice_question func, else use just say something and return a boolean response
        #to the guiven channel in the first message
        #Note: The one that guive us the first instruction should be subscribed to the same channel that he give us to recibe the response.
        print(message)

if __name__ == "__main__":
    main()