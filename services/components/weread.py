import reflex as rx
import httpx
from enum import Enum
from lib.weread2notion.main import Weread_async
from sqlmodel import select
from services.login_service import LoginState
from Model.Vip import Vip
from data.vip_data import Vip_type, VipBase
import os
class TaskStatus(Enum):
    CONNECT_NOTION = 0
    GETWEREAD_COOKIE = 1
    RUN_SYNC = 2

class WereadState(rx.State):
    notion_link = "https://api.notion.com/v1/oauth/authorize?client_id=1fad872b-594c-8143-9186-003750ff3168&response_type=code&owner=user&redirect_uri=https%3A%2F%2Fcdmstrong.github.io%2F"
    _n_tasks: int = 0 
    access_token: str = ""
    vip_info: VipBase = VipBase()

    @rx.event
    def get_weread(self):
        
        # 获取cookie, 账户名，密码，要么传入密钥
        with rx.session() as session:
            statement = select(Vip).where(
                (Vip.user_id == LoginState.user.user_id) & (Vip.vip_type == Vip_type.WEREAD))
            result = session.exec(statement)
            vip = result.first()
            if not vip:
                return 
            self.vip_info = vip

    @rx.event
    def save_data(self, data: dict):
        self.access_token = data.get("token", "")
        self.notion_page = data.get("page_id", "")
        self.weread_cookie = data.get("cookie", "")
        # 更新到数据库
        with rx.session() as session:
            statement = select(Vip).where(
                (Vip.user_id == LoginState.user.user_id) & (Vip.vip_type == Vip_type.WEREAD))
            result = session.exec(statement)
            vip = result.first()
            if not vip:
                return 
    @property
    def weread(self):
        vip = self.vip_info
        return Weread_async(vip.weread_cookie, vip.cc_id, vip.cc_password, vip.notion_token, vip.notion_page)
    
    @rx.event
    async def run_bind_notion(self):
        # 绑定notion
        # get_access_token()

        # get_page_id()
        pass

    @rx.event(background=True)
    async def run_weread(self):
        # 同步书籍，同步笔记，同步时间
        async with self:
            if self._n_tasks > 0:
                return  # 避免重复任务
            self._n_tasks += 1
            self.weread.start_sync()

