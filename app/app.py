import reflex as rx
from pages import login, home

app = rx.App()
app.add_page(login.page)
app.add_page(home.page)