from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import uuid
class UserBase(BaseModel):
    email: str = ""
    username: str = ""
    password: str = ""
    user_id: Optional[int] 
    is_admin: Optional[bool] = False
    start_time: Optional[datetime] = None #会员开始日期
    end_time: Optional[datetime] = None #会员结束日期
    register_time: Optional[datetime] = None #注册时间
    recharge_count: Optional[int] = 0


def uuid_to_int(in_id: str) -> int:
    return int(in_id.replace("-", ""), 16)


class UserLogin(UserBase):
    # is_active: bool = False
    class Config:
        from_attributes = True  # 启用 ORM 模式