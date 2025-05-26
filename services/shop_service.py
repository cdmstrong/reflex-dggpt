
import reflex as rx
from datetime import datetime
from data.shop_data import OrderInfo, ProductBase
from lib.alipay_lib.alipay_server import AlipayServer

class ShopService(rx.State):
    product_list: list[ProductBase] = [
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

    def alipay_server(self):
        return AlipayServer()
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.alipay_server = AlipayServer()
        # self.get_product_list()
    # 获取产品列表
    def get_product_list(self):

        return self.product_list
    @rx.event
    def close_qr_dialog(self):
        self.show_qr_dialog = False
        self.alipay_server.cancel_order(self.pay_order.order_id)
    @rx.event
    def set_product(self, product: ProductBase):
        self.product = product
        # self.show_qr_dialog = True
        self.show_buy_dialog = True
        self.product_count = 1
    @rx.event
    def close_buy_dialog(self):
        self.show_buy_dialog = False
    @rx.event
    def set_product_count(self, product_count: int):
        self.product_count = product_count

    @rx.event
    def buy_product(self, product: ProductBase ):
        
        # 生成购买链接
        # 生成购买二维码
        retry_count = 0
        while retry_count < 3:
            res = self.alipay_server.PreCreate(product.name, product.price * (1 - product.discount))
            if res:
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
                )
                self.show_qr_dialog = True
                break
            else:
                retry_count += 1




