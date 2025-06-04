from datetime import datetime
import uuid
from sqlmodel import Field
import reflex as rx
from reflex_local_auth import LocalUser
from sqlalchemy import Column, DateTime, func

class User(rx.Model, table=True):
    __tablename__ = "user"
    user_id: int = Field(foreign_key="localuser.id")
    username: str
    password: str
    email: str
    is_admin: bool = Field(default=False)
    register_time: datetime = Field(
        sa_column=Column(DateTime, nullable=False, server_default=func.now())
    )
    recharge_count: int = Field(default=0) # 充值次数 默认为0
   