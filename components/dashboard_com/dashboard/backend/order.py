from Model.Vip import Vip
from sqlmodel import select, delete, update
import reflex as rx
from data.vip_data import VipManager, VipSchema

class OrderManagerState(rx.State):
    order_list: list[VipSchema] = []

    order: VipManager = VipManager()
    is_add: bool = False
    is_edit: bool = False

    def get_data(self):
        self.get_order_list()

    def get_order_list(self):
        with rx.session() as session:
            res = session.exec(select(Vip)).all()
            self.order_list = [VipSchema.from_orm(order) for order in res]


    @rx.event
    def delete_order(self, vip_id: int):
        with rx.session() as session:
            session.exec(delete(Vip).where(Vip.vip_id == vip_id))
            session.commit()
            self.get_order_list()

    @rx.event
    def edit_order(self, vip_id: int):
        order = next((order for order in self.order_list if order.vip_id == vip_id), None)
        if order:
            self.order = VipManager(**order.model_dump())
            self.is_edit = True

    @rx.event
    def set_order_property(self, property_name: str, value: str):
        setattr(self.order, property_name, value)

    @rx.event
    def add_order(self):
        with rx.session() as session:

            session.add(self.order)
            session.commit()
            self.get_order_list()
            self.is_add = False
            rx.toast.success("添加成功")

    @rx.event
    def update_order(self):
        with rx.session() as session:
            session.exec(update(Vip).where(Vip.vip_id == self.order.vip_id).values(self.order.model_dump()))
            session.commit()
            self.get_order_list()
            self.is_edit = False
            rx.toast.success("编辑成功")

    @rx.event
    def toggle_add(self):
        self.is_add = not self.is_add

    @rx.event
    def toggle_edit(self):
        self.is_edit = not self.is_edit

