from sqlmodel import Field
import reflex as rx

class Product(rx.Model, table=True):
    __tablename__ = "product"
    product_id: int = Field(default=None, primary_key=True)
    name: str
    image: str
    price: float
    description: str
    time: int = Field(default=0)
    discount: float = Field(default=0)
    type: int = Field(default=1)
   