from datetime import datetime
import uuid
from sqlmodel import Field
import reflex as rx
from reflex_local_auth import LocalUser

class User(rx.Model, table=True):
    __tablename__ = "user"
    user_id: int = Field(foreign_key="localuser.id")
    username: str
    password: str
    email: str
    is_admin: bool = Field(default=False)
    start_time: datetime = Field(default=None) # 开始时间 默认为空
    end_time: datetime = Field(default=None) # 结束时间 默认为空
    register_time: datetime = Field(default=datetime.now()) # 注册时间 默认为当前时间
    recharge_count: int = Field(default=0) # 充值次数 默认为0
   