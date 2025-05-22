
import reflex as rx
from data.user_data import UserLogin
from Model.User import User
from datetime import timedelta
import reflex_local_auth
from reflex_local_auth import LocalUser
from sqlmodel import select
class LoginState(reflex_local_auth.LocalAuthState):
    user: UserLogin = UserLogin(username="", password="", user_id="", email="", is_admin=False, start_time=None, end_time=None, register_time=None)
    error_message: str = ""
    in_login: bool = True

    def on_load(self):
        if not self.is_authenticated:
            return rx.redirect("/login")
        self.data = f"欢迎，{self.authenticated_user.username}！这是您的私人数据。"
    @rx.event
    async def login(self):
        # await self.get_var_value(AuthState.username)
        # user_state = await self.get_state(UserState)
        with rx.session() as session:
            statement = select(User).where(
                (User.username == self.user.username) & (User.password == self.user.password))
            result = session.exec(statement)
            user = result.first()
        if user :
            self._login(user.id, expiration_delta=timedelta(days=2))
            self.error_message = None
        else:
            self.error_message = "用户名或密码错误"
    @rx.event
    def toggle_register(self):
        self.in_login = not self.in_login
        
    @rx.event
    def register(self):
        with rx.session() as session:
            session.add(
                User(
                    username=self.user.username, email=self.user.email, password=self.user.password, is_admin=False
                )
            )
            session.commit()
        self.in_login = True


    @rx.event
    def logout(self):
        self.username = ""
        self.password = ""
        self.error_message = None
        self.do_logout()
        return rx.redirect("/login")

    @rx.event
    def set_username(self, username: str):
        self.user.username = username

    @rx.event
    def set_password(self, password: str):
        self.user.password = password

    @rx.event
    def set_email(self, email: str):
        self.user.email = email
