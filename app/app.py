import reflex as rx
from routes import index
# db
from Model.User import User

app = rx.App()

app.add_page(index.home_route)
app.add_page(index.login_route)