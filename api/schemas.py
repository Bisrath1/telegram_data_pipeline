from pydantic import BaseModel

class ProductFrequency(BaseModel):
    product: str
    count: int

class ChannelActivity(BaseModel):
    channel_name: str
    total_messages: int
    with_images: int

class MessageSearchResult(BaseModel):
    message_id: int
    message_text: str
    channel_name: str
    message_date: str
