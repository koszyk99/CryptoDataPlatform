{{ config(materialized='table') }}

SELECT 
    symbol,
    AVG(price) AS avg_price,
    date_trunc('minutes', timestamp) AS minute_bucket
FROM {{ source('raw', 'crypto_prices') }}
GROUP BY symbol, minute_bucket
ORDER BY minute_bucket DESC
