import reflex as rx
from services.components.weread import WereadState
def use_weread():
    # 关联notion
    rx.box(
        rx.heading("步骤1：关联notion"),
        rx.hstack(
            rx.text("点击关联notion"),
            rx.link(WereadState.notion_link, target="_blank"),
        )
        
    )