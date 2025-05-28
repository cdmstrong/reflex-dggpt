import reflex as rx
import reflex_local_auth

from pages.components.buy import buy_product_com
from pages.components.vip_product_page import vip_product_page
from services.login_service import LoginState
from services.vip_service import VipService
class HomeState(rx.State):
    value = "buy"

    @rx.event
    def on_tab_change(self, val):
        self.value = val
        if val == "relevance":
            # 这里写 vip_product_page 需要初始化的逻辑
            VipService.get_vip_list()

def top_bar():
    return rx.box(
        rx.text("状态栏", font_size="20px", font_weight="bold"),
        bg="teal",
        color="white",
        padding="1em",
        height="60px",
        width="100%",
        box_shadow="md",
    )

def side_bar():
    return rx.vstack(
        rx.text("标签1"),
        rx.text("标签2"),
        rx.text("标签3"),
        spacing="1",
        align_items="start",
        padding="1em",
        bg="gray.100",
        height="100%",
        width="200px",
        border_right="1px solid #ccc",
    )

def content_area():
    return rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("产品购买", value="buy"),
                rx.tabs.trigger("产品关联", value="relevance"),
                spacing="2",
                align_items="start",
                padding="1em",
                bg="gray.100",
                height="100%",
                width="200px",
                border_right="1px solid #ccc",
            ),
            
            rx.tabs.content(
                buy_product_com(),
                value="buy",
                padding="2em",
            ),
            rx.tabs.content(
                vip_product_page(),
                value="relevance",
                padding="3em",

            ),
            default_value="buy",
            orientation="vertical",
            height="calc(100vh - 60px)",
            padding="1em",
            value=HomeState.value,
            on_change=HomeState.on_tab_change,
    )

@rx.page(route="/home")
@reflex_local_auth.require_login
def home_page():
    
    return rx.box(
        top_bar(),
        rx.hstack(
            # side_bar(),
            content_area(),
            # right_content(),
            height="calc(100vh - 60px)",  # 减去状态栏高度
        ),
        width="100%",
        height="100vh",
    )

def top_bar():
    # 布局是，最左侧显示name：东哥科技，最右侧显示个人头像（底部显示：名称，悬浮显示退出，联系客服(悬浮显示客服二维码)
    return rx.box(
        rx.box(rx.text("东哥科技", font_size="20px", font_weight="bold")),
        rx.box(
            rx.hstack(
                rx.text(LoginState.user.username, font_size="16px", font_weight="bold"),
                rx.vstack(
                    rx.hover_card.root(
                        rx.hover_card.trigger(
                            rx.avatar(src=rx.asset("concat.png"), size="2", style=cursor_style),
                        ),
                        rx.hover_card.content(
                            rx.text("退出", font_size="13px", font_weight="bold", on_click=LoginState.logout, style=cursor_style),
                        ),
                    ),
                    spacing="1",
                    padding="1em 1em 1em 0",
                ),
                rx.hover_card.root(
                    rx.hover_card.trigger(
                        rx.text("联系客服", font_size="16px", font_weight="bold", style=cursor_style),
                        
                    ),
                    rx.hover_card.content(
                        rx.image(src=rx.asset("qr_code.png"), width="100px")
                    ),
                ),
                align_items="center",
                padding="1em 1em",
            ),
        ),
        bg="teal",
        color="white",
        display="flex",
        justify_content="space-between",
        align_items="center",
        padding="1em 3em",
        height="60px",
    )
# 左边的菜单栏购买


cursor_style = {
    "cursor": "pointer",
}