from typing import Optional
from pydantic import BaseModel
class Location(BaseModel):
    id: int
    has_public_page: bool = False
    name: Optional[str]
    slug: Optional[str]
    address_json: Optional[str]