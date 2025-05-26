from collections import deque
import reflex as rx

from pages import login, home
# db
from Model.User import User
from Model.Product import Product
from Model.Vip import Vip

from fastapi import FastAPI, Request
fastapi_app = FastAPI(title="My API")


@fastapi_app.get("/api/get_token")
async def get_items(request: Request):
    # 获取request的query参数
    query = request.query_params
    print(query)
    return dict(items=["Item1", "Item2", "Item3"])

app = rx.App(api_transformer=fastapi_app)

app.add_page(home.home_page)
app.add_page(login.login_page)