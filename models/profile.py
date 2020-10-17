from pydantic import BaseModel
from typing import Optional


class Profile(BaseModel):
    id: int
    username: str
    full_name: str
    biography: Optional[str]
    profile_pic_url: Optional[str]

    amount_posts: int = 0
    amount_followers: int = 0
    amount_following: int = 0

    connected_to_fb_page: bool = False
    connected_fb_page: Optional[str]

    external_url: Optional[str]

    is_joined_recently: bool = False
    is_private: bool = False
    is_verified: bool = False

    is_business_account: bool = False
    business_email: Optional[str]
    business_category_name: Optional[str]
    category_enum: Optional[str]
