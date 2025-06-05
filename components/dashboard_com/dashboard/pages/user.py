
from ..views.table import product_modal, product_table, add_product
from .. import styles
from ..templates import template
import reflex as rx

# 产品管理页面
from data.shop_data import ProductSchema
from Model.Product import Product
from ..backend.user import UserManagerState
from ..views.user import user_table

@template(route="/user", title="用户管理", on_load=UserManagerState.get_data)
def user() -> rx.Component:
    # 产品管理页面
    return rx.vstack(
        rx.heading("用户管理"),
        user_table(),
        spacing="8",
        width="100%",
    )

