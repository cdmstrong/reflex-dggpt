
import functools
import re
import reflex as rx
from data.user_data import UserLogin
from Model.User import User
from datetime import timedelta
import datetime
import reflex_local_auth
from reflex_local_auth import LocalUser
from sqlmodel import select

DEFAULT_AUTH_REFRESH_DELTA = datetime.timedelta(minutes=10)

class LoginState(reflex_local_auth.LocalAuthState):
    user: UserLogin = UserLogin(username="", password="", user_id=None, email="", is_admin=False, start_time=None, end_time=None, register_time=None)
    error_message: str = ""
    in_login: bool = True
    is_admin: bool = False

    @rx.var(cache=True, interval=DEFAULT_AUTH_REFRESH_DELTA)
    def user_is_admin(self) -> bool:
        return self.user.is_admin
    @rx.var(cache=True, interval=DEFAULT_AUTH_REFRESH_DELTA)
    def user_info(self) -> UserLogin:
        """The currently authenticated user, or a dummy user if not authenticated.

        Returns:
            A LocalUser instance with id=-1 if not authenticated, or the LocalUser instance
            corresponding to the currently authenticated user.
        """

        with rx.session() as session:
            statement = select(User).where(
                (User.user_id == self.authenticated_user.id)
            )
            result = session.exec(statement)
            user = result.first()
            if user:
                self.user = UserLogin.from_orm(user)
                # print(f"user_info: {self.user}")
                return self.user
            else:
                return UserLogin(username="", password="", user_id=None, email="", is_admin=False, start_time=None, end_time=None, register_time=None)
    @rx.event
    def toggle_admin(self):
        self.is_admin = not self.is_admin

    @rx.event
    async def login(self):
        # await self.get_var_value(AuthState.username)
        # user_state = await self.get_state(UserState)
        with rx.session() as session:
            statement = select(User).where(
                (User.email == self.user.email) & (User.password == self.user.password))
            result = session.exec(statement)
            user = result.first()
        if user:
            # print(user.id)
            self._login(user.id, expiration_delta=timedelta(days=2))
            self.error_message = ""
            if self.is_admin:
                self.user.is_admin = True
                return rx.redirect("/admin/")
            else:
                return rx.redirect("/home")
        else:
            self.error_message = "用户名或密码错误"
    @rx.event
    def toggle_register(self):
        self.in_login = not self.in_login
        
    @rx.event
    def register(self):
        with rx.session() as session:
            # 查询邮箱是否存在
            statement = select(User).where(User.email == self.user.email)
            result = session.exec(statement)
            user = result.first()
            if user:
                self.error_message = "邮箱已存在"
                return
            localuser = LocalUser(
                username=self.user.username, password_hash=LocalUser.hash_password(self.user.password), enabled=True
            )
            session.add(localuser)
            session.commit()
            session.refresh(localuser)
            user = User(
                id = localuser.id,
                username=self.user.username,
                email=self.user.email,
                password=self.user.password,
                user_id=localuser.id,
                is_admin=False
            )
            session.add(user)
            session.commit()
        self.in_login = True


    @rx.event
    def logout(self):
        # self.user.username = ""
        # self.user.password = ""
        self.error_message = ""
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

    @rx.var
    def invalid_email(self) -> bool:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'
        if re.match(pattern, self.user.email):
            return False
        else:
            return True


def require_admin(page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:
    """Decorator to require authentication before rendering a page.

    If the user is not authenticated, then redirect to the login page.

    Args:
        page: The page to wrap.

    Returns:
        The wrapped page component.
    """

    def protected_page():
        return rx.fragment(
            rx.cond(
                LoginState.user_is_admin,  # type: ignore
                page(),
                rx.center(
                    # When this text mounts, it will redirect to the login page
                    rx.text("无法进入管理员界面，请先登录", on_mount=rx.redirect("/login")),
                ),
            )
        )

    protected_page.__name__ = page.__name__
    return protected_page