
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
                return UserLogin.from_orm(user)
            else:
                return UserLogin(username="", password="", user_id=None, email="", is_admin=False, start_time=None, end_time=None, register_time=None)
            
    @rx.event
    async def login(self):
        # await self.get_var_value(AuthState.username)
        # user_state = await self.get_state(UserState)
        with rx.session() as session:
            statement = select(User).where(
                (User.email == self.user.email) & (User.password == self.user.password))
            result = session.exec(statement)
            user = result.first()
        if user :
            # print(user.id)
            self._login(user.id, expiration_delta=timedelta(days=2))
            self.error_message = ""
            return rx.redirect("/home")
        else:
            self.error_message = "用户名或密码错误"
    @rx.event
    def toggle_register(self):
        self.in_login = not self.in_login
        
    @rx.event
    def register(self):
        with rx.session() as session:
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
