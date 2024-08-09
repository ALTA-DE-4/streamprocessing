from confluent_kafka import Producer
from datetime import datetime
import random
import json
import uuid
# from config import TOPIC

TOPIC="has_stock_json_topic"
def produce():
    # Configure the Producer
    p = Producer({
        'bootstrap.servers': '34.101.224.54:19092',  # Assuming you're running this on the same machine as the compose
        'client.id': 'has_python-producer'
    })

    # Produce a message
    countdata = 0
    try:
        while True:
            stock = {
                'event_time': datetime.now().isoformat(),
                'ticker': random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV']),
                'price': round(random.random() * 100, 2)
            }
            p.produce(TOPIC, key=str(uuid.uuid4), value=json.dumps(stock), callback=delivery_report)
            countdata+=1
            if countdata == 2000:
                break;
            else:
                pass
    except Exception as e:
        print(str(e))

    # Wait for any outstanding messages to be delivered
    p.flush()

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def main():
    produce()

if __name__ == "__main__":
    main()
    
