import reflex as rx
from services.login_service import LoginState

@rx.page(route="/login")
def login_page():
    return rx.box(
        # 顶部标题
        rx.heading(
            "东哥科技",
            size="9",
            color="#1A237E",
            margin_bottom="68px",
            align="center",
        ),
        # 居中登录面板
        rx.center(
            rx.box(
                rx.vstack(
                    rx.heading("登录", size="4", margin_bottom="24px"),
                    
                    rx.form.root(
                        rx.cond(
                            ~LoginState.in_login,
                            rx.form.field(
                                rx.form.label("用户名"),
                                rx.form.control(
                                    rx.input(placeholder="用户名", on_change=LoginState.set_username, value=LoginState.user.username),
                                    as_child=True,
                                ),
                                rx.form.message(
                                    "请输入用户名",
                                    match="valueMissing",
                                    force_match=LoginState.user.username == "",
                                    color="var(--red-11)",
                                ),
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("邮箱"),
                            rx.form.control(
                                rx.input(
                                    placeholder="邮箱",
                                    on_change=LoginState.set_email,
                                    name="email",
                                    type="email",
                                ),
                                as_child=True,
                            ),
                            rx.form.message(
                                "请输入正确的邮箱格式",
                                match="valueMissing",
                                force_match=LoginState.invalid_email,
                                color="var(--red-11)",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("密码"),
                            rx.form.control(
                                rx.input(placeholder="密码", type="password", on_change=LoginState.set_password, value=LoginState.user.password),
                                as_child=True,
                            ),  
                            rx.form.message(
                                "请输入密码",
                                match="valueMissing",
                                force_match=LoginState.user.password == "",
                                color="var(--red-11)",
                            ),
                        ),
                    ),
                    rx.checkbox(
                        "管理员登录",
                        on_change=LoginState.toggle_admin,
                        is_checked=LoginState.is_admin,
                    ),
                    rx.cond(
                        LoginState.in_login,
                        rx.hstack(
                            rx.link("注册", on_click=LoginState.toggle_register),
                            rx.button("登录", on_click=LoginState.login),
                        ),
                    ),
                    
                    rx.cond(
                        ~LoginState.in_login,
                        rx.hstack(
                            rx.button("注册", on_click=LoginState.register),
                            rx.link("登录", on_click=LoginState.toggle_register),
                            text_align = "center",
                            align_items="center",
                        )
                    ),
                    rx.cond(
                        LoginState.error_message,
                        rx.text(LoginState.error_message, color="red"),
                    ),
                    spacing="4",
                    align="center",
                ),
                box_shadow="0 4px 24px rgba(0,0,0,0.12)",
                border_radius="12px",
                padding="40px 32px",
                bg="white",
                min_width="320px",
            ),
            # height="calc(100vh - 158px)",  # 预留顶部标题空间
        ),
        concat_page(),
        width="100vw",
        height="100vh",
        display="flex",
        flex_direction="column",
        justify_content="center",
        align_items="center",
        bg="#f5f6fa",
    )

def concat_page():
    return rx.box(
            rx.text("联系客服", color="#000000", font_size="16px", font_weight="bold", margin_bottom="10px"),
            rx.hover_card.root(
                rx.hover_card.trigger(
                    rx.avatar(src=rx.asset("concat.png"), size="5")
                ),
                rx.hover_card.content(
                    rx.image(src=rx.asset("qr_code.png"), width="100px")
                ),
            
            ),
            style = {
                    "position":"fixed",
                    "right":"160px",
                    "zIndex": "1000"
            }
        )

