from data.shop_data import ProductAdd, ProductSchema
from Model.Product import Product
from sqlmodel import select, delete, update
import reflex as rx

class ProductManagerState(rx.State):
    product_list: list[ProductSchema] = []

    product: ProductAdd = ProductAdd()
    is_add: bool = False
    is_edit: bool = False
    def get_data(self):
        self.get_product_list()
    @rx.event
    def toggle_add(self):
        self.is_add = not self.is_add

    def get_product_list(self):
        with rx.session() as session:
            res = session.exec(select(Product)).all()
            self.product_list = [ProductSchema.from_orm(product) for product in res]
    @rx.event
    def update_product(self):
        with rx.session() as session:
            session.exec(update(Product).where(Product.product_id == self.product.product_id).values(name=self.product.name, image=self.product.image, description=self.product.description, price=self.product.price, discount=self.product.discount, type=self.product.type))
            session.commit()
            self.get_product_list()
            self.is_add = False
            self.is_edit = False
            rx.toast.success("编辑成功")

    @rx.event
    def add_product(self):
        if self.product.image is None:
            rx.toast.error("请上传图片")
            return
        product = Product(name=self.product.name, image=self.product.image, description=self.product.description, price=self.product.price, discount=self.product.discount, type=self.product.type)
        with rx.session() as session:
            session.add(product)
            session.commit()
            self.get_product_list()
            self.is_add = False
            rx.toast.success("添加成功")
    @rx.event
    def edit_product(self, product_id: int):
        self.is_edit = True
        product = next((product for product in self.product_list if product.product_id == product_id), None)
        if product:
            self.product = ProductAdd(**product.model_dump())
        self.is_add = True

    @rx.event
    def delete_product(self, product_id: int):
        with rx.session() as session:
            session.exec(delete(Product).where(Product.product_id == product_id))
            session.commit()
            self.get_product_list()
            rx.toast.success("删除成功")

    @rx.event
    def set_product_property(self, property_name: str, value: str):
        if not value:
            return
        setattr(self.product, property_name, value)

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            data = await file.read()
            path = rx.get_upload_dir() / file.name
            with path.open("wb") as f:
                f.write(data)
            self.product.image = file.name
            rx.toast.success("上传成功")
    @rx.event
    def clear_uploaded_images(self):
        self.product.image = ""

