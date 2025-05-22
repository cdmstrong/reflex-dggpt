import reflex as rx
import reflex_local_auth

@reflex_local_auth.require_login
def home_page():
    
    return rx.center(
        rx.heading("欢迎来到主页！", size="8"),
        height="100vh"
    )

