import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username: str
    password: str
    user_id: str
    is_admin: bool
    start_time: datetime #会员开始日期
    end_time: datetime #会员结束日期
    register_time: datetime #注册时间
    

class UserLogin(UserBase):
    is_active: bool
