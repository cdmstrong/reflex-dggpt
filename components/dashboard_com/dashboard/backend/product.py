from data.shop_data import ProductSchema
from Model.Product import Product
from sqlmodel import select
import reflex as rx

class ProductManagerState(rx.State):
    product_list: list[ProductSchema] = []

    def get_data(self):
        self.get_product_list()

    def get_product_list(self):
        with rx.session() as session:
            res = session.exec(select(Product)).all()
            self.product_list = [ProductSchema.from_orm(product) for product in res]