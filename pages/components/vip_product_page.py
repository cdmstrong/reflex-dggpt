# 使用产品
import reflex as rx

from services.vip_service import VipService


def vip_product_page():

    return rx.box(
        # 遍历列表展示
            rx.heading("产品列表", size="5", margin_bottom="1em"),  
            rx.flex(
                rx.foreach(VipService.vip_list, lambda product: rx.card(
                    rx.vstack(
                        rx.text(product.product_name, bold=True, size="3"),
                        rx.text(f"有效期{product.startTime} - {product.endTime}", size="3", color="red"),
                        
                        rx.button("配置", on_click=VipService.use_product(product)),

                        align="start", 
                        justify="center",
                    ),
                    padding="2em",
                    align="start",
                    border_radius="1em",
                    border="1px solid #ccc",
                    box_shadow="0 0 10px 0 rgba(0, 0, 0, 0.1)",
                    width="250px",
                    height="400px",
                ),
            ),
            spacing="4",
            width="100%",
        ),
        padding="2em",
        margin="2em",
    )