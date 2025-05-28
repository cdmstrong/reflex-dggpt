
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import uuid
from enum import Enum


class Vip_type(Enum):
    WEREAD = 1


class VipBase(BaseModel):
    type: int = Vip_type.WEREAD.value
    startTime: datetime = None 
    endTime: datetime = None
    vip_id: int = None
    notion_token: Optional[str] = None
    weread_cookie: Optional[str] = None
    notion_page: Optional[str] = None
    cc_id: Optional[str] = None
    cc_password: Optional[str] = None
    product_name: Optional[str] = None



class VipSchema(VipBase):

    class Config:
        from_attributes = True