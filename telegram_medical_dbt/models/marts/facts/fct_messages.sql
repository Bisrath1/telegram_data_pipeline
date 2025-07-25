<<<<<<< HEAD
with dates as (
  select distinct date::date as full_date from {{ ref('stg_telegram_messages') }}
)

select
  full_date,
  extract(year from full_date) as year,
  extract(month from full_date) as month,
  extract(day from full_date) as day,
  extract(dow from full_date) as day_of_week,
  to_char(full_date, 'Day') as weekday_name
from dates

{{ config(materialized='view') }}

SELECT
    message_id,
    channel_id,
    CAST(sent_at AS TIMESTAMP) AS sent_at,
    LENGTH(message_text) AS message_length,
    CASE
        WHEN media_json IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS has_image
FROM {{ ref('stg_telegram_messages') }}
=======
with src as (
    select *
    from {{ ref('stg_telegram_messages') }}
),

joined as (
    select
        s.message_id,
        d.date,
        c.channel_id,
        s.message_text,
        length(s.message_text)       as message_length,
        s.has_image,
        s.image_path
    from src           s
    left join {{ ref('dim_channels') }} c
        on s.channel_name = c.channel_name
    left join {{ ref('dim_dates') }}    d
        on cast(s.message_date as date) = d.date
)

select * from joined
>>>>>>> 7fe380ed3ca4754af7f51164ab7491d24702def4
