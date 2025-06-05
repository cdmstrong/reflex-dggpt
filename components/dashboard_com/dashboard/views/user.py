
import reflex as rx
from .table import _header_cell
from data.user_data import UserSchema
from ..backend.user import UserManagerState
def _show_user_item(item: UserSchema, index: int) -> rx.Component:
    
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
        rx.table.row_header_cell(item.username),
        rx.table.cell(item.email),
        rx.table.cell(item.register_time),
        rx.table.cell(item.is_admin),
        rx.table.cell(item.recharge_count),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    "升级为管理员",                    
                    on_click=UserManagerState.upgrade_to_admin(item.user_id),
                ),
                rx.button(
                    "降级",
                    on_click=UserManagerState.downgrade_to_user(item.user_id),
                )
            )
        ),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def user_table() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                _header_cell("用户名", "user"),
                _header_cell("邮箱", "dollar-sign"),
                _header_cell("创建时间", "calendar"),
                _header_cell("状态", "notebook-pen"),
                _header_cell("管理", "notebook-pen"),
            ),
        ),
        rx.table.body(
            rx.foreach(
                UserManagerState.user_list,
                lambda item, index: _show_user_item(item, index),
            )
        ),
        variant="surface",
        size="3",
        width="100%",           
    )

