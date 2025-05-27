from collections import deque
from fastapi.responses import HTMLResponse
import reflex as rx
from pages import login, home
# db
from Model.User import User
from Model.Product import Product
from Model.Vip import Vip

from utils.weread import get_access_token, get_page_id
from fastapi import FastAPI, Request

from services.components.weread import WereadState
import os
from dotenv import load_dotenv

load_dotenv(override=True)

fastapi_app = FastAPI(title="My API")


@fastapi_app.get("/api/get_token")
async def get_items(request: Request):
    # 获取request的query参数
    query = request.query_params
    print(query)
    # 获取code
    code = query.get("code")
    try:
        access_token = await get_access_token(code)
        page_id = await get_page_id(access_token)

        html_content = f""" 
        <html>
            <head><title>绑定成功</title></head>
            <body>
                <div style="text-align: center; align-items: center; margin: 0 auto;">
                    <h1>绑定成功！</h1>
                    <p style="padding: 10px;"> 你的access_token是：<strong>{access_token}</strong></p>
                    <p style="padding: 10px;">你的 Page ID 是：<strong>{page_id}</strong></p>
                </div>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)

    except Exception as e:
        print(e)
    

app = rx.App(api_transformer=fastapi_app)

app.add_page(home.home_page)
app.add_page(login.login_page)