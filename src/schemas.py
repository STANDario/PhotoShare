from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class PostSingle(BaseModel):
    img: str
    id: int
    url_original: str
    description: Optional[str]
    pub_date: datetime

    class ConfigDict:
        from_attributes = True
