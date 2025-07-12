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
