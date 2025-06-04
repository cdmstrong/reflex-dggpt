import reflex as rx
from services.components.weread import WereadState
from services.states.vip import WereadStepState, VipProductPageState

def my_tip(tip):
    return rx.box(
        tip,
        background_color=rx.color("gray", 1),
        border=f"1px solid {rx.color('gray', 4)}",
        border_radius="8px",
        padding="12px",
        width="100%",
    )


def logs_page():
    return rx.cond(
        WereadState.show_process_log,
        rx.box(
            rx.text_area(
                value= WereadState.process_log,
                rows="10",
                resize="vertical",
                width="100%",
            ),
            rx.button(
                "关闭",
                on_click=WereadState.toggle_process_log,
            ),
            rx.moment(
                interval=2000,
                on_change=WereadState.refresh,
                format="HH:mm:ss",  # 格式随意，只要触发 on_change 就行
                display="none",     # 如果不想显示内容
            )
        )
        
    )
def step_content(step_label):
    return rx.box(
        # rx.text(f"{step_label}"),
        rx.cond(
            WereadStepState.current_step == "step1",
            rx.vstack(
                rx.heading("方法1：直接复制微信读书的cookie", size="5"),
                rx.link("前往weread(需要不定期更新cookie)", href="https://weread.qq.com/"),
                rx.hstack(
                    rx.text("cookie:"),
                    rx.input(
                        value= WereadStepState.step_data.get("cookie", ""),
                        on_change= lambda v: WereadStepState.save_step_data("cookie", v),
                    ),
                ),
                rx.heading("方法2：使用cookieCloud的自动同步功能", size="5"),
                rx.link(
                    "CookieCloud插件",
                    href="https://chromewebstore.google.com/detail/cookiecloud/ffjiejobkoibkjlhjnlgmcnnigeelbdl",
                ),
                my_tip(f"配置服务器为：{WereadStepState.cookie_cloud}, 参考cookie 配置文档"),
                rx.hstack(
                    rx.text("uu_id:"),
                    rx.input(
                        value= WereadStepState.step_data.get("cookie_cloud_user_id", ""),
                        on_change= lambda v: WereadStepState.save_step_data("cookie_cloud_user_id", v),
                    ),
                ),
                rx.hstack(
                    rx.text("password:"),
                    rx.input(
                        value= WereadStepState.step_data.get("cookie_cloud_password", ""),
                        on_change= lambda v: WereadStepState.save_step_data("cookie_cloud_password", v),
                    ),
                ),
                spacing="2",
                padding="0.1rem",
            )
        ),
        rx.cond(
            WereadStepState.current_step == "step2",
            rx.vstack(
                my_tip("请先绑定notion，然后复制获得的token和pageid"),
                rx.link(
                    "获取token和page_id",
                    href="https://api.notion.com/v1/oauth/authorize?client_id=1fad872b-594c-8143-9186-003750ff3168&response_type=code&owner=user&redirect_uri=https%3A%2F%2Fapi.dggpt.top%2Fapi%2Fget_token",
                ),
                rx.hstack(
                    rx.text("notion token:"),
                    rx.input(
                        value= WereadStepState.step_data.get("token", ""),
                        on_change= lambda v: WereadStepState.save_step_data("token", v),
                    ),
                ),
                rx.hstack(
                    rx.text("page_id:"),
                    rx.input(
                        value= WereadStepState.step_data.get("page_id", ""),
                        on_change= lambda v: WereadStepState.save_step_data("page_id", v),
                    ),
                ),
                spacing="2",
                padding="0.1rem",
            )
        ),
        rx.cond(
            WereadStepState.current_step == "step3",
            rx.vstack(
                rx.text_area(
                    value= WereadState.process_log,
                    rows="10",
                    resize="vertical",
                    width="100%",
                ),
                rx.hstack(
                    rx.button(
                        "保存",
                        on_click=[
                            WereadState.save_data(WereadStepState.step_data),
                        ],
                        margin_top="0.3rem",
                    ),
                ),
                my_tip("系统默认会在每天00:00同步数据"),
                spacing="2",
                padding="0.1rem",
            ),
            
        ),
    )

def weread_process_flow():
    steps = [f"step{i}" for i in range(1, 4)]
    # labels = [f"步骤{i}" for i in range(1, 6)]
    labels = ["获取cookie", "获取token和page_id", "开始同步"]
    return rx.tabs.root(
            rx.tabs.list(
                *[rx.tabs.trigger(label, value=step) for label, step in zip(labels, steps)]
            ),
            *[rx.tabs.content(
                step_content(label),
                value=step,
                padding="2em"
            ) for label, step in zip(labels, steps)],
            value=WereadStepState.current_step,
            on_change=WereadStepState.go_to_step,
            default_value="step1",
            orientation="vertical",
        )