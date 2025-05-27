import reflex as rx
from services.login_service import LoginState
import httpx
import os

class TokenState(rx.State):
    # 定义查询参数
    code: str = ""
    access_token: str = ""
    page_id: str = ""
    error: str = ""
    
    @rx.event(background=True)
    async def get_query_params(self):
        """获取查询参数"""
        # 获取当前 URL 的查询参数
        query_params = self.router.page.params
        self.code = query_params.get("code", "")
        print(self.code)
        if self.code:
            await self.get_access_token()
            if self.access_token:
                await self.get_page_id()

    

@rx.page(route="/bind_weread")
def get_token_page():
    return rx.box(
        rx.text("绑定微信读书..."),
        rx.cond(
            TokenState.error,
            rx.text(TokenState.error, color="red"),
        ),
        rx.cond(
            TokenState.access_token,
            rx.vstack(
                rx.text("Access Token:"),
                rx.text(TokenState.access_token),
                rx.text("Page ID:"),
                rx.text(TokenState.page_id),
                rx.text("请复制以上信息到网站使用"),
                spacing="3",
            ),
            rx.text("正在获取授权信息..."),
        ),
        on_mount=TokenState.get_query_params,
        padding="2em",
    )