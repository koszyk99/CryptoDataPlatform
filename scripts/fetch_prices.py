import requests
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from confluent_kafka import Producer

# Choose which coin we want to track
coins = ['bitcoin', 'ethereum', 'solana', 'cardano']
ids_param = ",".join(coins)

# Read .env file
load_dotenv()

db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_name = os.getenv('POSTGRES_DB')

# Create Kafka Producer
conf = {'bootstrap.servers': "localhost:9094"}
producer = Producer(conf)

# Function that tell us if it was successful
def message_delivery(err, msg):
    if err is not None:
        print(f"Sending error: {err}")
    else:
        print(f"Sending to {msg.topic()} [{msg.partition()}]")

print("Starting price fetcher... Press CTRL + C to stop.\n")

try:
    while True:
        # Fetch data from API
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={ids_param}&vs_currencies=usd')
        print(response.url)

        if response.status_code == 200:
            data = response.json()

            # Loop for data and sending to Kafka
            for coin_id, coin_info in data.items():
                symbol = coin_id.upper()
                price = coin_info['usd']
                timestamp = datetime.now().isoformat()

                # Create data packages (dictoinary -> JSON)
                payload = {
                    'symbol': symbol,
                    'price': price,
                    'timestamp': timestamp
                }

                # Send to Kafka
                producer.produce(
                    'crypto-topic',
                    json.dumps(payload).encode('utf-8'),
                    callback=message_delivery
                )

            # We are waiting for confirmation that all messagees have been sent
            producer.flush()
            print("Batch sent. Waiting 10 seconds...\n")
        else:
            print(f"API error: {response.status_code}")

        time.sleep(10)

except KeyboardInterrupt:
    print("\nStopping price fetcher. Goodbye!")
