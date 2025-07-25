-- models/marts/telegram/mart_user_activity.sql

WITH user_messages AS (
  SELECT
    user_id,
    COUNT(*) AS message_count,
    MIN(timestamp) AS first_message_time,
    MAX(timestamp) AS last_message_time
  FROM {{ ref('stg_messages') }}
  GROUP BY user_id
)

SELECT
  u.user_id,
  u.username,
  u.joined_at,
  um.message_count,
  um.first_message_time,
  um.last_message_time
FROM {{ ref('stg_users') }} u
LEFT JOIN user_messages um ON u.user_id = um.user_id
