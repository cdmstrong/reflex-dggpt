

import reflex as rx
from data.vip_data import VipSchema

import os

from lib.weread2notion.main import Weread_async
from services.vip_service import VipService
from utils.scheduler import SchedulerManager 
def scheduler_job(vip: VipSchema):
        weread_async = Weread_async(vip.weread_cookie, vip.cc_id, vip.cc_password, vip.notion_token, vip.notion_page, vip.vip_id)
        weread_async.start_sync()

class VipProductPageState(rx.State):
    is_show_product_page: bool = True
    product: VipSchema = None

    @rx.event
    def use_product(self, product: VipSchema):
        # VipService.use_product(product)
        self.product = product
        print(f"product: {product}")
        self.is_show_product_page = False
        vip = VipService.get_vip_by_id(self.product.vip_id)
        print(f"use_product: {vip}")
        if not vip:
            return
        SchedulerManager.add_cron_job(scheduler_job, vip.vip_id, hour=24, kwargs={"vip": vip})

    @rx.event
    def show_product_page(self):
        self.is_show_product_page = True


class WereadStepState(rx.State):
    current_step: str = "step1"
    cookie_cloud: str = os.getenv("COOKIE_CLOUD")
    # 用于存储每个步骤的数据
    step_data: dict = {}

    @rx.event
    def go_to_step(self, step):
        self.current_step = step

    @rx.event
    def save_step_data(self, step, data):
        if not data:
            return
        self.step_data[step] = data