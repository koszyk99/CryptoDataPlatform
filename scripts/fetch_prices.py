import requests
import json
import os
import time
import socket
from datetime import datetime
from dotenv import load_dotenv
from confluent_kafka import Producer

# Choose which coin we want to track
coins = ['bitcoin', 'ethereum', 'solana', 'cardano']
ids_param = ",".join(coins)

# Read .env file
load_dotenv()

# FIX: Wait for Kafka to be actually ready before connecting
# depends_on in docker-compose only waits for the container to START, not for Kafka to be READY
def wait_for_kafka(host, port, timeout=120):
    print(f"Waiting for Kafka at {host}:{port}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=2):
                print("Kafka is ready!")
                return
        except OSError:
            time.sleep(3)
    raise RuntimeError(f"Kafka not available after {timeout}s — giving up.")

kafka_host = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092').split(':')
wait_for_kafka(kafka_host[0], int(kafka_host[1]))

# Create Kafka Producer
conf = {'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')}
producer = Producer(conf)

# Callback: tells us if the message was delivered successfully
def message_delivery(err, msg):
    if err is not None:
        print(f"Delivery error: {err}")
    else:
        print(f"Sent to {msg.topic()} [partition {msg.partition()}]")

print("Starting price fetcher... Press CTRL+C to stop.\n")

try:
    while True:
        try:
            response = requests.get(
                f'https://api.coingecko.com/api/v3/simple/price?ids={ids_param}&vs_currencies=usd',
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                for coin_id, coin_info in data.items():
                    payload = {
                        'symbol': coin_id.upper(),
                        'price': coin_info['usd'],
                        'timestamp': datetime.now().isoformat()
                    }
                    producer.produce(
                        'crypto-topic',
                        json.dumps(payload).encode('utf-8'),
                        callback=message_delivery
                    )

                producer.flush()
                print("Batch sent. Waiting 30 seconds...\n")

            else:
                print(f"API error: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        time.sleep(30)

except KeyboardInterrupt:
    print("\nStopping price fetcher. Goodbye!")
