<<<<<<< HEAD
{{ config(materialized='view') }}

SELECT DISTINCT
    channel_id,
    'Unknown Channel' AS channel_name -- you can later enrich this
FROM {{ ref('stg_telegram_messages') }}
=======
with source as (
    select distinct channel_name
    from {{ ref('stg_telegram_messages') }}
),

final as (
    select
        row_number() over (order by channel_name) as channel_id,
        channel_name
    from source
)

select * from final
>>>>>>> 7fe380ed3ca4754af7f51164ab7491d24702def4
