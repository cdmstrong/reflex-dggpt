from pydantic import BaseModel
from typing import Optional

from data.vip_data import Vip_type

class ProductBase(BaseModel):
    product_id: Optional[int] = None
    name: Optional[str] = None
    image: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    time: Optional[int] = None
    discount: Optional[float] = None
    type: Optional[int] = 1

class ProductSell(ProductBase):
    pass
class ProductAdd(ProductBase):
    name: str = ""
    price: float = 0
    description: str = ""
    discount: float = 0
    type: int = 1

class ProductSchema(ProductBase):
    class Config:
        from_attributes = True
# 订单信息
class OrderInfo(BaseModel):
    order_id: str
    product_id: int
    product_name: str
    product_price: float
    product_time: str = None
    product_discount: float
    is_pay: bool = False
    pay_time: Optional[str] = None
    pay_qr_code: Optional[str] = None
    pay_link: Optional[str] = None
    pay_type: Optional[Vip_type] = Vip_type.WEREAD.value
