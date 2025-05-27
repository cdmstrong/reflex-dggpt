import base64
import time
import uuid
import qrcode
from alipay import AliPay

# Initialize FastMCP server
from dotenv import load_dotenv
import os
import time, random

load_dotenv()
current_dir = os.path.dirname(__file__)
# 单例支付类
class AlipayServer:

    _instance = None
    is_init = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AlipayServer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if self.is_init:
            return
        self.is_init = True
        self.ALIPAY_APPID = os.getenv("ALIPAY_APPID")
        self.APP_PRIVATE_KEY = open(f"{current_dir}/key/app_private_key.pem").read()
        self.ALIPAY_PUBLIC_KEY = open(f"{current_dir}/key/alipay_public_key.pem").read()

        self.alipay=AliPay(appid=self.ALIPAY_APPID, ##appid，用沙箱的话会给你个
                    app_notify_url=None,   ##默认回调url，需要外网才能跳转，
                    app_private_key_string=self.APP_PRIVATE_KEY,  ##本地私钥
                    ##支付宝的公钥，验证支付回传消息时使用,不是自己生成的公钥，
                    alipay_public_key_string=self.ALIPAY_PUBLIC_KEY,
                    )


    def get_qr_code(self, code_url):
        """
        生成二维码
        :param code_url:  创建预付订单时生成的code_url
        :return:
        """
        qr=qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1,
        )
        qr.add_data(code_url) ##二维码所含信息(支付地址等)
        img=qr.make_image()   ##生成二维码图片
        # 生成随机uuid
        id = str(uuid.uuid4())
        img_path = f'{os.getenv("STATIC_PATH")}/qr_code/qr_{id}.png'
        img.save(img_path)
        # 返回base64编码的图片
        # with open(img_path, 'rb') as image_file:
        #     return base64.b64encode(image_file.read()).decode('utf-8')
        return f'qr_code/qr_{id}.png'

    def get_out_trade_no(self):

        prefix = "Time"  # 可选商户自定义前缀
        timestamp = int(time.time() * 1000)  # 毫秒级时间戳，避免秒级冲突
        rand_part = random.randint(1000, 9999)

        out_trade_no = f"{prefix}{timestamp}{rand_part}"
        print(out_trade_no)  # 示例：ALI17143841234561234
        return out_trade_no

    def generate_out_request_no(self, order_id: str) -> str:
        """
        为同一逻辑订单生成多个唯一支付宝订单号（out_trade_no）
        :param order_id: 你的业务主订单号，例如 ORD12345
        :return: 唯一支付宝订单号
        """
        timestamp = int(time.time() * 1000)  # 毫秒级时间戳
        rand_part = random.randint(100, 999)
        return f"{order_id}_{timestamp}{rand_part}"
    
    def PreCreate(self, subject, total_amount:float):
        """
        创建预付订单；alipay.trade.precreate
        :param subject:     str    商品名称
        :param total_amount:     float 价格
        :return: markdown 文本
        """
        out_trade_no = self.get_out_trade_no()
        result=self.alipay.api_alipay_trade_precreate(
            subject=subject,
            out_trade_no=out_trade_no,
            total_amount=total_amount)
        print('返回值',result)
        code_url=result.get('qr_code')  ##qr_code:创建预付订单成功时返回的："qr_code": "https://qr.alipay.com/bax03431ljhokirwl38f00a7"

        if  not code_url:
            print('预付订单创建失败：',result.get('msg'))
            return None
        else:
            print('预付订单创建成功：',result.get('msg'))
            ##如果时success response的话去执行get_qr_code函数
            base64_qr_code = self.get_qr_code(code_url)   ##生成一个带有qr_code信息的二维码
            # print(base64_qr_code)
            return {
                    "out_trade_no":out_trade_no,
                    "total_amount":total_amount,
                    "subject":subject,
                    "pay_url":code_url,
                    "qr_code":base64_qr_code
                }
            
    def query_order(self, out_trade_no: str):
        """
        订单状态查询：alipay.trade.query
        :param out_trade_no: str 商户订单号以Time开头
        :return: 订单支付状态
        :cancel_time: int 设置的支付时间
        """
        trade_status = False
        result=self.alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        if result.get("trade_status","")=="TRADE_SUCCESS":
            print('订单已支付')
            trade_status = True
        print('订单查询返回值：',result.get("trade_status",""))
        if trade_status:
            return True
        else:
            return False
    
    
    def cancel_order(self, out_trade_no: str):
        """
        撤销订单：alipay.trade.cancel
        :param out_trade_no: str 商户订单号以Time开头
        :return:

        assert (out_trade_no is not None) or (trade_no is not None),\
                "Both trade_no and out_trade_no are None"
        订单号out_trade_no不能为空
        """
        result=self.alipay.api_alipay_trade_cancel(out_trade_no=out_trade_no)
        resp_status=result.get('msg')
        if  resp_status=="Success":  #撤销成功
            print('撤销成功')
            return True       
        else:
            print('请求失败',resp_status)
            return False
    
    def roll_refund(self, out_trade_no: str, refund_amount: float):

        """
        退款操作：alipay.trade.refund
        :param out_trade_no:   str     商户订单号以Time开头
        :param refund_amount: float      退款金额，小于等于订单金额, 单位: 元, 例如 0.4
        :return: result 或 error message
        """
        out_request_no = self.generate_out_request_no(out_trade_no)
        print(out_trade_no, refund_amount, out_request_no)
        result = self.alipay.api_alipay_trade_refund(out_trade_no=out_trade_no,
                                            refund_amount=refund_amount,
                                            out_request_no=out_request_no)
        print(result)
        if  result['code']=="10000":#调用成功则返回result
            return result
        else:
            return None #接口调用失败则返回msg

    def fastpay_refund(self, out_trade_no: str, out_request_no:str):
        """
        统一交易退款查询：alipay.trade.fastpay.refund.query
        :param out_trade_no: str 商户订单号以Time开头
        :param out_request_no: str 商户自定义的单次退款请求标识符以Time开头
        :return: result 或 error message
        """
        result=self.alipay.api_alipay_trade_fastpay_refund_query(out_trade_no=out_trade_no,out_request_no=out_request_no)
        print(result)
        if  result['code']=='10000':
            return result
        else:
            return None



if __name__ == '__main__':
    ##创建预订单
    ##商品名称
    subject='蚂蚁矿机'
    # ##订单号
    # out_trade_no=int(time.time())  ##将当前时间的时间戳转化为整型用做订单号
    # ##价格
    # total_amount=0.01
    # PreCreate(subject=subject,total_amount=0.01)
    out_trade_no='Time17479890133909587'
    alipay_server = AlipayServer()
    print(alipay_server.PreCreate(subject=subject, total_amount=0.01))
    print(alipay_server.query_order(out_trade_no))
    # print(alipay_server.cancel_order(out_trade_no))
    # print(alipay_server.roll_refund(out_trade_no, 0.01))
    # print(alipay_server.fastpay_refund(out_trade_no, out_request_no))

