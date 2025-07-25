with date_range as (
    select
        generate_series(
            date '2024-01-01',
            date '2025-12-31',
            interval '1 day'
        ) as date_day
),

final as (
    select
        date_day as date,
        extract(year from date_day) as year,
        extract(month from date_day) as month,
        to_char(date_day, 'Month') as month_name,
        extract(day from date_day) as day,
        extract(dow from date_day) as day_of_week,
        to_char(date_day, 'Day') as day_name,
        date_trunc('week', date_day)::date as week_start_date
    from date_range
)



select * from final


{{ config(materialized='view') }}

SELECT DISTINCT
    CAST(sent_at AS DATE) AS date,
    EXTRACT(YEAR FROM sent_at) AS year,
    EXTRACT(MONTH FROM sent_at) AS month,
    EXTRACT(DAY FROM sent_at) AS day,
    EXTRACT(DOW FROM sent_at) AS weekday
FROM {{ ref('stg_telegram_messages') }}
