{{ config(materialized='table') }}

with messages as (
    select * from {{ ref('stg_messages') }}
),

user_activity as (
    select
        user_id,
        count(*) as total_messages,
        min(created_at) as first_message_time,
        max(created_at) as last_message_time
    from messages
    group by user_id
)

select * from user_activity
