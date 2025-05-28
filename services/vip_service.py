
import reflex as rx
from datetime import datetime, timedelta
from Model import Vip
from data.shop_data import OrderInfo, ProductBase
from data.vip_data import Vip_type, VipSchema
from lib.alipay_lib.alipay_server import AlipayServer
from sqlmodel import select
class VipService(rx.State):

    # 是否显示所有产品页面
    is_show_product_page: bool = True


    vip_list: list[VipSchema] = []
    
    def get_vip_list(self):
        with rx.session() as session:
           statement = select(Vip)
           result = session.exec(statement)
           self.vip_list = result.all()

        return self.vip_list
    
    
    def get_vip_by_id(self, vip_id: int):
        return next((vip for vip in self.vip_list if vip.id == vip_id), None)

    def use_product(self, vip_id: int):
        pass