# 使用产品
import datetime
import reflex as rx

from data.vip_data import VipSchema
from pages.weread.use_vip import logs_page, weread_process_flow
from services.components.weread import WereadState
from services.states.vip import VipProductPageState, WereadStepState
from services.vip_service import VipService
from data.vip_data import Vip_type
from utils.common import format_time

def vip_product_page():
    return rx.box(
        rx.heading("产品列表", size="6", margin_bottom="1.5em", color="teal"),
        rx.cond(
            ~VipProductPageState.is_show_product_page,
            rx.button("返回", on_click=VipProductPageState.show_product_page, color_scheme="teal", variant="soft", margin_bottom="1.5em"),
        ),
        rx.cond(
            VipProductPageState.is_show_product_page,
            rx.flex(
                rx.foreach(
                    VipService.vip_list,
                    lambda product: rx.card(
                        rx.vstack(
                            rx.image(
                                src="/image.png",  # 可替换为 product.image
                                width="100px",
                                height="100px",
                                border_radius="0.5em",
                                margin_bottom="1em",
                                box_shadow="md",
                            ),
                            rx.text(product.product_name, bold=True, size="4", color="teal"),
                            rx.text("有效期", size="2", color="gray"),
                            rx.hstack(
                                rx.text(f"{product.start_time}", color="green", size="2"),
                                rx.text("—", color="gray", size="2"),
                                rx.text(f"{product.end_time}", color="red", size="2"),
                                spacing="2",
                            ),
                            rx.divider(margin_y="0.7em"),
                            rx.hstack(
                                rx.button("配置", on_click=VipProductPageState.use_product(product), color_scheme="teal", variant="solid"),
                                rx.button("立即同步", on_click=[
                                    WereadState.toggle_process_log(),
                                    WereadState.run_weread(),
                                ], color_scheme="blue", variant="outline"),
                                rx.button("查看日志", on_click=[
                                    WereadState.toggle_process_log(),
                                ], color_scheme="gray", variant="ghost"),
                                spacing="2",
                                width="100%",
                                justify="center",
                                align="center",
                            ),
                            align="center",
                            spacing="2",
                        ),
                        padding="1.5em",
                        align="center",
                        border_radius="1em",
                        border="1px solid #e0e0e0",
                        box_shadow="0 4px 24px 0 rgba(0, 0, 0, 0.08)",
                        width="280px",
                        min_height="420px",
                        transition="box-shadow 0.2s",
                        _hover={"box_shadow": "0 8px 32px 0 rgba(0, 0, 0, 0.16)", "border": "1.5px solid #38b2ac"},
                        background="white",
                        margin="1em",
                    ),
                ),
                wrap="wrap",
                gap="2em",
                justify="start",
            ),
        ),
        rx.cond(
            ~VipProductPageState.is_show_product_page,
            rx.box(
                rx.cond(
                    VipProductPageState.product.type == Vip_type.WEREAD.value,
                    weread_process_flow(),
                ),
            ),
        ),
        rx.cond(
            WereadState.show_process_log,
            logs_page()
        ),
        padding="2em",
        margin="2em",
        # background="#f8fafc",
        min_height="100vh",
    )