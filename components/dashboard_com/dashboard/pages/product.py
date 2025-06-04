
from ..views.table import product_table
from .. import styles
from ..templates import template
import reflex as rx
from sqlmodel import select
# 产品管理页面
from data.shop_data import ProductSchema
from Model.Product import Product
from ..backend.product import ProductManagerState


@template(route="/product", title="产品管理", on_load=ProductManagerState.get_data)
def product() -> rx.Component:
    # 产品管理页面
    return rx.vstack(
        rx.heading("产品管理"),
        product_table(),
        spacing="8",
        width="100%",
    )

