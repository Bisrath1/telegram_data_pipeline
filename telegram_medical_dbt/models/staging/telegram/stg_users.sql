{{ config(materialized='view') }}

with source as (
    select * from {{ source('telegram', 'users') }}
),

renamed as (
    select
        id as user_id,
        username,
        join_date
    from source
)

select * from renamed
