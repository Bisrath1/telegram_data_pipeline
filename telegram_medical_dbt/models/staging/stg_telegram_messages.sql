{{ config(materialized='view') }}

SELECT
    CAST(message->>'id' AS INTEGER) AS message_id,
    message->>'text' AS message_text,
    message->>'date' AS sent_at,
    message->>'sender_id' AS sender_id,
    message->>'chat_id' AS channel_id,
    message->>'media' AS media_json
FROM {{ source('raw', 'telegram_messages') }}
