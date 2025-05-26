from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    product_id: int
    name: str
    image: str
    price: float
    description: str
    time: Optional[int] = None
    discount: Optional[float] = None

class ProductSell(ProductBase):
    pass

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
