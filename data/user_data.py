from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    id: Optional[str] = None
    email: str = ""
    username: str = ""
    password: str = ""
    user_id: Optional[str] = ""
    is_admin: Optional[bool] = False
    start_time: Optional[datetime] = None #会员开始日期
    end_time: Optional[datetime] = None #会员结束日期
    register_time: Optional[datetime] = None #注册时间
    recharge_count: Optional[int] = 0

class UserLogin(UserBase):
    is_active: bool = False
