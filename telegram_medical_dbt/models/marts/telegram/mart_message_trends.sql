{{ config(materialized='table') }}

with messages as (
    select * from {{ ref('stg_messages') }}
),

daily_counts as (
    select
        date_trunc('day', created_at) as message_date,
        count(*) as total_messages
    from messages
    group by message_date
)

select * from daily_counts order by message_date
