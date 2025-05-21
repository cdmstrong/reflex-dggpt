import reflex as rx

def home_page():
    return rx.center(
        rx.heading("欢迎来到主页！", size="8"),
        height="100vh"
    )

page = rx.page(route="/home")(home_page)