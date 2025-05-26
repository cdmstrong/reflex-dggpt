import reflex as rx
import httpx
from enum import Enum
from lib.weread2notion.main import Weread_async
from sqlmodel import select
from services.login_service import LoginState
from Model.Vip import Vip
from data.vip_data import Vip_type
class TaskStatus(Enum):
    CONNECT_NOTION = 0
    GETWEREAD_COOKIE = 1
    RUN_SYNC = 2

class WereadState(rx.State):
    notion_link = "https://api.notion.com/v1/oauth/authorize?client_id=1fad872b-594c-8143-9186-003750ff3168&response_type=code&owner=user&redirect_uri=https%3A%2F%2Fcdmstrong.github.io%2F"
    _n_tasks: int = 0 
    weread: Weread_async
    def __init__(self):
        pass

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
            
        self.weread = Weread_async(vip.weread_cookie, vip.cc_id, vip.cc_password, vip.notion_token, vip.notion_page)
        return self.weread
    
    @rx.event(background=True)
    async def run_weread(self):
        # 同步书籍，同步笔记，同步时间
        async with self:
            if self._n_tasks > 0:
                return  # 避免重复任务
            self._n_tasks += 1
            self.weread.start_sync()

def access_redict():
    
    # https://yourapp.com/oauth/callback?code=AUTHORIZATION_CODE
    # 获取code
    pass


def get_access_token():
#     curl -X POST https://api.notion.com/v1/oauth/token \
#   -H "Content-Type: application/json" \
#   -d '{
#     "grant_type": "authorization_code",
#     "code": "AUTHORIZATION_CODE",
#     "redirect_uri": "YOUR_REDIRECT_URI",
#     "client_id": "YOUR_CLIENT_ID",
#     "client_secret": "YOUR_CLIENT_SECRET"
#   }'
#     q_json = {
#     "grant_type": "authorization_code",
#     "code": "AUTHORIZATION_CODE",
#     "redirect_uri": "http://43.153.7.130:8000/api/get_token",
#     
#   }
#     httpx.post("https://api.notion.com/v1/oauth/token", json=q_json)

#     return access_token, bot_id
    pass


def get_page_id():
#     curl -X POST https://api.notion.com/v1/search \
#   -H "Authorization: Bearer ACCESS_TOKEN" \
#   -H "Notion-Version: 2022-06-28" \
#   -H "Content-Type: application/json" \
#   -d '{}'
    pass
