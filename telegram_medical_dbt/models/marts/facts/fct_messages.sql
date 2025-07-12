with src as (
    select *
    from {{ ref('stg_telegram_messages') }}
),

joined as (
    select
        s.message_id,
        d.date,
        c.channel_id,
        s.message_text,
        length(s.message_text)       as message_length,
        s.has_image,
        s.image_path
    from src           s
    left join {{ ref('dim_channels') }} c
        on s.channel_name = c.channel_name
    left join {{ ref('dim_dates') }}    d
        on cast(s.message_date as date) = d.date
)

select * from joined
