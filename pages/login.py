import reflex as rx

class LoginState(rx.State):
    username: str = ""
    password: str = ""
    error: str = ""

    @rx.event
    def login(self):
        # 简单校验，实际可接数据库
        if self.username == "admin" and self.password == "123456":
            print("登录成功")
            return rx.redirect("/home")
            
        else:
            self.error = "用户名或密码错误11"

def login_page():
    return rx.center(
        rx.box(
            rx.vstack(
                rx.heading("登录", size="4"),
                rx.input(placeholder="用户名", on_change=LoginState.set_username),
                rx.input(placeholder="密码", type_="password", on_change=LoginState.set_password),
                rx.button("登录", on_click=LoginState.login),
                rx.text(LoginState.error, color="red"),
                spacing="4",
                align="center",
            ),
            box_shadow="0 4px 24px rgba(0,0,0,0.12)",
            border_radius="12px",
            padding="40px 32px",
            bg="white",
            min_width="320px",
        ),
        height="100vh",
        bg="#f5f6fa"
    )

page = rx.page(route="/login")(login_page)