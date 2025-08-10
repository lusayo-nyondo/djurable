from quixstreams import Application
import os

app = Application(broker_address=os.getenv('KAFKA_BROKER', 'localhost:9092'))
topic = app.topic(os.getenv('STREAM_TOPIC', 'events'))

@app.topic_consumer(topic)
def handle_event(msg):
    print('Received:', msg.value())

if __name__ == '__main__':
    app.run()
