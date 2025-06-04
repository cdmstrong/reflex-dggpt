
import reflex as rx
from datetime import datetime, timedelta
from Model.Vip import Vip
from data.shop_data import OrderInfo, ProductBase
from data.vip_data import Vip_type, VipSchema
from lib.alipay_lib.alipay_server import AlipayServer
from sqlmodel import select

from services.login_service import LoginState

class VipService(rx.State):

    # 是否显示所有产品页面
    vip_list: list[VipSchema] = []
    
    @rx.event
    async def get_vip_list(self):
        print("get_vip_list")
        user = await self.get_var_value(LoginState.user)
        print(f"user_id: {user.user_id}")
        with rx.session() as session:
           statement = select(Vip).where(Vip.user_id == user.user_id)
           result = session.exec(statement)
           vip_list = result.all()
        print(f"vip_list: {vip_list}")
        # 转换成VipSchema
        self.vip_list = [VipSchema.from_orm(vip) for vip in vip_list]
    
    
    def get_vip_by_id(self, vip_id: int):
        return next((vip for vip in self.vip_list if vip.id == vip_id), None)

    def use_product(self, vip_id: int):
        pass