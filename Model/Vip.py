from datetime import datetime
import uuid
from sqlmodel import Field
import reflex as rx
from reflex_local_auth import LocalUser
from sqlalchemy import Column, DateTime, func
class Vip(rx.Model, table=True):
    __tablename__ = "vip"
    user_id: int = Field(foreign_key="user.id")
    vip_id: int =  Field(default=None, primary_key=True)
    cc_id: str =  Field(default=None)
    cc_password: str =  Field(default=None)
    start_time: datetime = Field(
        sa_column=Column(DateTime, nullable=True, server_default=func.now())
    )
    end_time: datetime = Field(
        sa_column=Column(DateTime, nullable=True)
    )
    register_time: datetime = Field(
        sa_column=Column(DateTime, nullable=False, server_default=func.now())
    )
    notion_token: str = Field(default=None)
    weread_cookie: str = Field(default=None)
    notion_page: str = Field(default=None)
    type: int = Field(default=None)
    product_name: str = Field(default=None)
    vip_price: float = Field(default=None)