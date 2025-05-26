
import reflex as rx
from services.login_service import LoginState

@rx.page(route="/bind_weread")
def get_token_page():
    return rx.text('bind')