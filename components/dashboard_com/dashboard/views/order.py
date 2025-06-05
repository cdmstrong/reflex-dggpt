
import reflex as rx
from .table import _header_cell
from ..backend.order import OrderManagerState
from data.vip_data import VipSchema
def _show_order_item(item: VipSchema, index: int) -> rx.Component:
    
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(item.vip_id),
        rx.table.cell(item.register_time),
        rx.table.cell(item.product_name),
        rx.table.cell(item.start_time),
        rx.table.cell(item.end_time),
        rx.table.cell(item.notion_token),
        rx.table.cell(item.weread_cookie),
        rx.table.cell(item.notion_page),
        rx.table.cell(item.cc_id),
        rx.table.cell(item.cc_password),
        rx.table.cell(item.vip_price),
        rx.table.cell(item.type),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    "删除",                    
                    on_click=OrderManagerState.delete_order(item.vip_id),
                ),
                rx.button(
                    "编辑",
                    on_click=OrderManagerState.edit_order(item.vip_id),
                )
            )
        ),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def order_table() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                _header_cell("订单id", "user"),
                _header_cell("下单时间", "dollar-sign"),
                _header_cell("名称", "calendar"),
                _header_cell("开始时间", "notebook-pen"),
                _header_cell("结束", "notebook-pen"),
                _header_cell("notion_token", "notebook-pen"),
                _header_cell("weread_cookie", "notebook-pen"),
                _header_cell("notion_page", "notebook-pen"),
                _header_cell("cc_id", "notebook-pen"),
                _header_cell("cc_password", "notebook-pen"),
                _header_cell("vip_price", "notebook-pen"),
                _header_cell("type", "notebook-pen"),
                _header_cell("操作", "notebook-pen"),
            ),
        ),
        rx.table.body(
            rx.foreach(
                OrderManagerState.order_list,
                lambda item, index: _show_order_item(item, index),
            )
        ),
        variant="surface",
        size="3",
        width="100%",           
    )

def order_modal():
    return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("添加产品"),
                rx.dialog.description("请填写产品信息"),
                edit_order(),
                rx.flex(
                    rx.cond(
                        OrderManagerState.is_edit,
                        rx.button("编辑", on_click=OrderManagerState.update_order),
                        rx.button("添加", on_click=OrderManagerState.add_order),
                    ),
                    rx.dialog.close(
                        rx.button("关闭")
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="450px",
            ),
            open=OrderManagerState.is_add,
            on_open_change=OrderManagerState.toggle_add,
    )

def edit_order() -> rx.Component:
    
    return rx.flex(
                # 点击加号上传图片，点击图片再次上传图片，上传好显示图片内容
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="订单id",
                    value=OrderManagerState.order.vip_id,
                    on_change=OrderManagerState.set_order_property("vip_id"),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="订单名称",
                    value=OrderManagerState.order.product_name,
                    on_change=OrderManagerState.set_order_property("product_name"),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="金额",
                    type="number",
                    value=OrderManagerState.order.vip_price ,
                    on_change=OrderManagerState.set_order_property("vip_price"),
                ),
                
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="产品类型，微信读书为1，kindle为2",
                    type="number",
                    value=OrderManagerState.order.type,
                    on_change=OrderManagerState.set_order_property("type"),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="notion_token",
                    type="number",
                    value=OrderManagerState.order.notion_token,
                    on_change=OrderManagerState.set_order_property("notion_token"),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="weread_cookie",
                    type="number",
                    value=OrderManagerState.order.weread_cookie,
                    on_change=OrderManagerState.set_order_property("weread_cookie"),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="notion_page",
                    type="number",
                    value=OrderManagerState.order.notion_page,
                    on_change=OrderManagerState.set_order_property("notion_page"),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="cc_id",
                    type="number",
                    value=OrderManagerState.order.cc_id,
                    on_change=OrderManagerState.set_order_property("cc_id"),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="cc_password",
                    type="number",
                    value=OrderManagerState.order.cc_password,
                    on_change=OrderManagerState.set_order_property("cc_password"),
                ),
                # rx.input(
                #     rx.input.slot(rx.icon("user")),
                #     placeholder="开始时间",
                #     type="time",
                #     value=OrderManagerState.order.start_time,
                #     on_change=OrderManagerState.set_order_property("start_time"),
                # ),
                # rx.input(
                #     rx.input.slot(rx.icon("user")),
                #     placeholder="结束时间",
                #     type="time",
                #     value=OrderManagerState.order.end_time,
                #     on_change=OrderManagerState.set_order_property("end_time"),
                # ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="注册时间",
                    type="text",
                    value=str(OrderManagerState.order.register_time),
                    read_only=True,
                    on_change=OrderManagerState.set_order_property("register_time"),
                ),
                
                spacing="3",
                direction="column",
                align="center",
                width="100%",
                padding="1rem",
            )
