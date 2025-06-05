
from ..views.order import order_modal, order_table
from .. import styles
from ..templates import template
import reflex as rx
from sqlmodel import select
# 产品管理页面
from ..backend.order import OrderManagerState


@template(route="/order", title="订单管理", on_load=OrderManagerState.get_data)
def order() -> rx.Component:
    # 产品管理页面
    return rx.vstack(
        rx.heading("订单管理"),
        # rx.button("添加产品", on_click=OrderManagerState.toggle_add),
        order_modal(),
        order_table(),
        spacing="8",
        width="100%",
    )

