<<<<<<< HEAD
with detections as (
    select
        detection_id,
        message_id,
        detected_object_class,
        confidence_score,
        detection_time
    from {{ ref('stg_image_detections') }}
),

messages as (
    select
        id as message_id,
        date as message_date,
        channel_id
    from {{ ref('fct_messages') }}
)

select
    d.detection_id,
    d.message_id,
    m.message_date,
    m.channel_id,
    d.detected_object_class,
    d.confidence_score,
    d.detection_time
from detections d
left join messages m on d.message_id = m.message_id
=======
{{ config(materialized='table') }}

SELECT
    id AS detection_id,
    message_id,
    detected_class,
    confidence
FROM {{ source('raw', 'image_detections') }}
>>>>>>> 7fe380ed3ca4754af7f51164ab7491d24702def4
