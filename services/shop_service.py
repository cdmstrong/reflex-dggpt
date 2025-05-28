import asyncio
import time
import reflex as rx
from datetime import datetime, timedelta
from Model.Product import Product
from Model.Vip import Vip
from data.shop_data import OrderInfo, ProductBase, ProductSchema
from lib.alipay_lib.alipay_server import AlipayServer
from services.login_service import LoginState
from dateutil.relativedelta import relativedelta
from sqlmodel import select
class ShopService(rx.State):
    product_list: list[ProductSchema] = [
        {
            "name": "微信读书",
            "product_id": 1,
            "image": "qr_code.png",
            "price": 1,
            "description": "这是微信读书关联notion的会员，可以享受微信读书的会员权益，并且可以同步到notion， 购买一个月起",
            "discount": 0.1,
            "time":1
        },
        {
            "name": "快捷指令记账",
            "image": "qr_code.png",
            "product_id": 2,
            "price": 1,
            "description": "快捷指令记账，可以记录每天的收入和支出，并且可以同步到notion， 购买一个月起",
            "discount": 0.1,
            "time": 1
        }
    ]
    show_qr_dialog: bool = False
    pay_order: OrderInfo = None
    product: ProductBase = None
    product_count: int = 1
    show_buy_dialog: bool = False
    # 订单剩余时间
    order_left_time: int = 600
    # 是否存在未支付订单
    is_order_exist: bool = False
    @property
    def alipay_server(self):
        return AlipayServer()
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.alipay_server = AlipayServer()
        # self.get_product_list()
    # 获取产品列表
    @rx.event
    def get_product_list(self):
        with rx.session() as session:
            statement = select(Product)
            result = session.exec(statement)
            self.product_list = result.all()
        return self.product_list
    @rx.event
    def close_qr_dialog(self):
        self.show_qr_dialog = False
        res = self.alipay_server.cancel_order(self.pay_order.order_id)
        if res:
            self.is_order_exist = False

    @rx.event
    def set_product(self, product: ProductBase):
        self.product = product
        self.show_qr_dialog = True
        # self.show_buy_dialog = True
        self.product_count = 1
    @rx.event
    def close_buy_dialog(self):
        self.show_qr_dialog = False
    @rx.event
    def set_product_count(self, product_count: int):
        self.product_count = product_count

    # 订单查询方法
    async def query_order(self, order_id: str):
        # 10分钟内每3s查询一次
        print("开始查询")
        while self.order_left_time > 0:
            if not self.is_order_exist:
                return None
            res = self.alipay_server.query_order(order_id)
            print(f"res order {res}")
            if res:
                async with self:
                    self.order_left_time = 600
                    self.is_order_exist = False
                    self.show_qr_dialog = False
                    self.pay_order.is_pay = True
                    login_state = await self.get_state(LoginState)
                    current_user_id = login_state.user.user_id
                    current_pay_type = self.pay_order.pay_type.value
                    current_product_name = self.pay_order.product_name
                    print(f"current_user_id: {current_user_id}, current_pay_type: {current_pay_type}, current_product_name: {current_product_name}")
                    await self.save_pay_order()
                return res
            await asyncio.sleep(2)
            async with self:
                self.order_left_time -= 3
        return None
    async def save_pay_order(self):
        try:
            # 正确获取 LoginState
            login_state = await self.get_state(LoginState)
            user_id = login_state.user.user_id
            
            # 获取订单相关信息
            pay_type = self.pay_order.pay_type.value  # 使用 .value 获取枚举值
            product_name = self.pay_order.product_name

            with rx.session() as session:
                vip_order = Vip(
                    user_id = user_id,
                    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    end_time = (datetime.now() + relativedelta(years=10)).strftime("%Y-%m-%d %H:%M:%S"),
                    type = pay_type,
                    product_name = product_name
                )
                session.add(vip_order)
                session.commit()
                print(f"订单保存成功: user_id={user_id}, type={pay_type}, product={product_name}")
        except Exception as e:
            print(f"保存订单时发生错误: {str(e)}")
    @rx.event(background=True)
    async def buy_product(self, product: ProductBase):
        
        # 生成购买链接
        # 生成购买二维码
        retry_count = 0
        while retry_count < 3:
            if self.is_order_exist:
                print("订单已存在")
                return 
            res = self.alipay_server.PreCreate(product.name, product.price * product.discount)
            if res:
                async with self:
                    self.pay_order = OrderInfo(
                        order_id=res["out_trade_no"],
                        product_id=product.product_id,
                        product_name=product.name,
                        product_price=product.price,
                        product_discount=product.discount,
                        product_time= datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        is_pay=False,
                        pay_time=None,
                        pay_qr_code=res["qr_code"],
                        pay_link=res["pay_url"],
                        pay_type = product.type
                    )
                    
                    self.is_order_exist = True
                    self.show_qr_dialog = True
                await self.query_order(self.pay_order.order_id)

                # self.show_buy_dialog = True
                break
            else:
                retry_count += 1

    @rx.event
    async def get_user_id(self):
        login_state = await self.get_state(LoginState)
        print(f"login_state: {login_state}")
        return login_state.user_info.user_id


