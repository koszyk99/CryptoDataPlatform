import requests
import json
import psycopg2
from dotenv import load_dotenv
import os

response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
print(response.url)
print(response.status_code)

# Convert a raw response from the internet into a Python dictionary
data = response.json()

# Fetch prices
price = data['bitcoin']['usd']
print(f"Success! Bitcoin price: {price} USD")

# read .env file
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
except Exception as e:
    print(f"Connection error: {e}")
