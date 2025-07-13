{{ config(materialized='table') }}

SELECT
    id AS detection_id,
    message_id,
    detected_class,
    confidence
FROM {{ source('raw', 'image_detections') }}
