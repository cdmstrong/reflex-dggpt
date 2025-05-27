import reflex as rx
from services.shop_service import ShopService

# 购买产品的界面


# 卡片产品显示， 然后点击后，弹窗显示购买二维码和购买链接
def buy_product_com():
    return rx.box(
        # 遍历列表展示
            rx.heading("产品列表", size="5", margin_bottom="1em"),  
            rx.flex(
                rx.foreach(ShopService.product_list, lambda product: rx.card(
                    rx.vstack(
                        rx.image(src=f"/{product.image}", width="160px", height="160px"),
                        rx.text(product.name, bold=True, size="3"),
                        rx.hstack( 
                            rx.text(f"￥{product.price * (1 - product.discount)}元", size="3", color="red"),
                            rx.text(f"￥{product.price}元", size="2", color="gray"),
                            spacing="1",
                            align="center",
                        ),
                        rx.text(product.description, size="2", color="gray",
                                 style={
                                "display": "-webkit-box",
                                "overflow": "hidden",
                                "WebkitLineClamp": 3,
                                "WebkitBoxOrient": "vertical",
                                "textOverflow": "ellipsis",
                                "whiteSpace": "normal",
                            }),
                        rx.button("购买", on_click=ShopService.buy_product(product)),

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
        qr_dialog(),
        padding="2em",
        margin="2em",
    )



def qr_dialog():
    return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("购买商品"),
                # rx.text("数量：", size="2", color="gray"),
                # rx.input(on_change=ShopService.set_product_count(), value=ShopService.product_count),
                # rx.button("购买", on_click=ShopService.buy_product),
                rx.text(ShopService.pay_order.product_name, size="2", color="gray"),
                rx.text(f"￥{ShopService.pay_order.product_price}元", size="2", color="red"),
                rx.image(src=rx.get_upload_url(ShopService.pay_order.pay_qr_code), width="200px"),
                rx.text(f"剩余时间{ShopService.order_left_time}秒", size="2", color="gray"),
                rx.dialog.close(
                        rx.button("关闭", size="3", on_click=ShopService.close_buy_dialog),
                ),
            ),
            open=ShopService.show_qr_dialog,
    )