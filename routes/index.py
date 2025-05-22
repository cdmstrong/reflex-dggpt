import reflex as rx
from pages.home import home_page
from pages.login import login_page

home_route = rx.page(route="/home")(home_page)
login_route = rx.page(route="/login")(login_page)