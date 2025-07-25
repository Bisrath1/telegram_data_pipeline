-- models/marts/telegram/mart_message_trends.sql

SELECT
  DATE_TRUNC('day', timestamp) AS message_date,
  COUNT(*) AS total_messages
FROM {{ ref('stg_messages') }}
GROUP BY 1
ORDER BY 1
