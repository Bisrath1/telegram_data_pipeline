{{ config(materialized='view') }}

SELECT DISTINCT
    channel_id,
    'Unknown Channel' AS channel_name -- you can later enrich this
FROM {{ ref('stg_telegram_messages') }}
