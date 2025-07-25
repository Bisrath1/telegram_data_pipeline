<<<<<<< HEAD
{{ config(materialized='view') }}

SELECT
    CAST(message->>'id' AS INTEGER) AS message_id,
    message->>'text' AS message_text,
    message->>'date' AS sent_at,
    message->>'sender_id' AS sender_id,
    message->>'chat_id' AS channel_id,
    message->>'media' AS media_json
FROM {{ source('raw', 'telegram_messages') }}
=======
with source as (
    select * from raw.telegram_messages
),

renamed as (
    select
        message_id,
        channel_name,
        message_text,
        CAST(message_date AS timestamp) as message_date,
        has_image,
        image_path,
        raw_json
    from source
)

select * from renamed
>>>>>>> 7fe380ed3ca4754af7f51164ab7491d24702def4
