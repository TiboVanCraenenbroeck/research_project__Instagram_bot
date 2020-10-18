from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class Post(BaseModel):
    id: int
    shortcode: str
    url: str
    likes: int
    comments: int
    caption: Optional[str]
    edge_media_to_caption: str
    is_video: bool = False
    location: Optional[str]
    time_stamp: datetime