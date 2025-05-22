
import reflex as rx
from compoments.auth import AuthState
from data.user_data import UserLogin

class LoginState(rx.State):
    user: UserLogin
    error: str = ""
    is_logged_in: bool = False  # 新增字段
    __auth_state = AuthState()

    @rx.event
    def login(self):
        if self.username == "admin" and self.password == "123456":
            # 特定方式加密成字符串，利用username和password生成一个唯一的字符串
            self.is_logged_in = True

            return rx.redirect("/home")
        else:
            self.error = "用户名或密码错误"

    def is_login(self):
        return self.is_logged_in
    
    @rx.event
    def logout(self):
        self.is_logged_in = False
        return rx.redirect("/login")
