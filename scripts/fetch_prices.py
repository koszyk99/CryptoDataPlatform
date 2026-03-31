import requests
import json
import psycopg2
from dotenv import load_dotenv
import os

# Choose which coin we want to track
coins = ['bitcoin', 'ethereum', 'solana', 'cardano']
ids_param = ",".join(coins)

# Data download
response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={ids_param}&vs_currencies=usd')
print(response.url)
print(response.status_code)

# Convert a raw response from the internet into a Python dictionary
data = response.json()

# Read .env file
load_dotenv()

db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD')
db_name = os.getenv('POSTGRES_DB')

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        host='localhost',
        password=db_pass,
        port='5432'
    )
    print(f"Connected to database: {db_name}")

    # Create cursor
    cur = conn.cursor()

    for coin_id, coin_info in data.items():
        price = coin_info['usd']
        symbol = coin_id.upper()

        # Execute method for sql query
        sql_query = "INSERT INTO raw_crypto_prices (symbol, price) VALUES (%s, %s)"
        cur.execute(sql_query, (symbol, price))
        print(f"I'm putting in: {symbol} - {price} USD")

    # "Save"
    conn.commit()

    # End work and close cursor
    cur.close()
    conn.close()

except Exception as e:
    print(f"Connection error: {e}")
