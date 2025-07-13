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
