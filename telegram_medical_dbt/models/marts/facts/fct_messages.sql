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
