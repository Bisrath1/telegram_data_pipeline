{{ config(materialized='view') }}

with source as (
    select * from {{ source('telegram', 'messages') }}
),

renamed as (
    select
        id as message_id,
        user_id,
        message_text,
        created_at
    from source
)

select * from renamed
