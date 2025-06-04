import reflex as rx
import httpx
from enum import Enum

from lib.weread2notion.main import Weread_async
from sqlmodel import update, select
from services.login_service import LoginState
from Model.Vip import Vip
from data.vip_data import Vip_type, VipBase, VipSchema
from datetime import timedelta

from services.states.vip import VipProductPageState
from utils.logs import VipLogManager

DEFAULT_AUTH_REFRESH_DELTA = timedelta(minutes=10)

class TaskStatus(Enum):
    CONNECT_NOTION = 0
    GETWEREAD_COOKIE = 1
    RUN_SYNC = 2

class WereadState(rx.State):
    notion_link = "https://api.notion.com/v1/oauth/authorize?client_id=1fad872b-594c-8143-9186-003750ff3168&response_type=code&owner=user&redirect_uri=https%3A%2F%2Fcdmstrong.github.io%2F"
    _n_tasks: int = 0 
    access_token: str = ""
    show_process_log: bool = False

    access_token: str = ""
    notion_page: str = ""
    weread_cookie: str = ""
    cc_id: str = ""
    cc_password: str = ""

    vip_info: VipSchema = VipSchema()
    # @rx.var(cache=True)
    # async def vip_info(self) -> VipSchema:
    #     # 获取cookie, 账户名，密码，要么传入密钥
    #     user = await self.get_var_value(LoginState.user)
    #     user_id = user.user_id
    #     with rx.session() as session:
    #         statement = select(Vip).where(
    #             (Vip.user_id == user_id) & (Vip.type == Vip_type.WEREAD.value))
    #         result = session.exec(statement)
    #         vip = result.first()
    #         if not vip:
    #             return VipSchema()
    #         return VipSchema.from_orm(vip)
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fetch_vip_info()
    # 计算属性
    tick: int = 0

    @rx.event
    def refresh(self):
        self.tick += 1
        
    @rx.var
    def process_log(self) -> str:
        _ = self.tick 
        return VipLogManager().get_log(self.vip_info.vip_id)
    
    @rx.event
    def add_log(self, log: str):
        print(f"self.vip_info.vip_id: {self.vip_info.vip_id}")
        print(f"add_log: {log}")
        VipLogManager().add_log(self.vip_info.vip_id, log)

    @rx.event
    def toggle_process_log(self):
        self.show_process_log = not self.show_process_log

    @rx.event
    async def fetch_vip_info(self):
        user = await self.get_var_value(LoginState.user)
        user_id = user.user_id
        print(f"user_id: {user_id}")
        # if hasattr(user_id, "value"):
            # user_id = user_id.value
        with rx.session() as session:
            statement = select(Vip).where(
                (Vip.user_id == user_id) & (Vip.type == Vip_type.WEREAD.value))
            result = session.exec(statement)
            vip = result.first()
            if not vip:
                self.vip_info = VipSchema()
            else:
                self.vip_info = VipSchema.from_orm(vip)
        return self.vip_info
    @rx.event
    async def save_data(self, data: dict):
        self.access_token = data.get("token", "")
        self.notion_page = data.get("page_id", "")
        self.weread_cookie = data.get("cookie", "")
        self.cc_id = data.get("cookie_cloud_user_id", "")
        self.cc_password = data.get("cookie_cloud_password", "")
        # 更新到数据库，如果字段有新的值，则更新，否则不更新
        user = await self.get_var_value(LoginState.user)
        print(f"user_id: {user.user_id}")
        
        with rx.session() as session:
            statement = update(Vip).where(Vip.user_id == user.user_id).values(
                notion_token=self.access_token,
                notion_page=self.notion_page,
                weread_cookie=self.weread_cookie,
                cc_id=self.cc_id,
                cc_password=self.cc_password
            )
            result = session.exec(statement)
            session.commit()  # 别忘了提交
            if result.rowcount > 0:
                print("保存成功")
                return rx.window_alert("保存成功")  
                # other_state = await self.get_state(VipProductPageState)
                # other_state.is_show_product_page = True
            else:
                print("没有任何行被更新（可能 user_id 不存在）")
                return rx.window_alert("保存失败")

    def weread(self, vip):
        try:
            return Weread_async(vip.weread_cookie, vip.cc_id, vip.cc_password, vip.notion_token, vip.notion_page, vip.vip_id)
        except Exception as e:
            print(e)
            # self.add_log(f"初始化失败失败: {e}")
            raise Exception("初始化失败 weread 失败")
    
    @rx.event
    async def run_bind_notion(self):
        # 绑定notion
        # get_access_token()

        # get_page_id()
        pass
    
    @rx.event(background=True)
    async def run_weread(self):
        # 只在这里判断和修改 _n_tasks
        try:
            async with self:
                if self._n_tasks > 0:
                    return
                self._n_tasks += 1
                vip_info = await self.fetch_vip_info()

                weread = self.weread(vip_info)
        # 在 context 外执行耗时操作（不会阻塞主线程/事件循环）
                self.add_log("开始同步微信读书")

            print(f"self.vip_info: {vip_info}")
            print("already init weread")
            await rx.run_in_thread(weread.start_sync)
        except Exception as e:
            # 捕获异常后再进入 context 修改 state
            print(e)
            async with self:
                self.add_log(f"初始化失败: {e}")
                self.show_process_log = True
                self._n_tasks -= 1
            return

        # 任务结束后，记得归零 _n_tasks
        async with self:
            self._n_tasks -= 1
                
