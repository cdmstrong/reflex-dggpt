from turtle import _PenState
import reflex as rx
from services.components.weread import WereadState
class WereadStepState(rx.State):
    current_step: str = "step1"
    # 用于存储每个步骤的数据
    step_data: dict = {}

    @rx.event
    def go_to_step(self, step):
        self.current_step = step

    @rx.event
    def save_step_data(self, step, data):
        self.step_data[step] = data

def step_content(step_label):
    return rx.box(
        rx.text(f"{step_label}"),
        rx.cond(
            WereadStepState.current_step == "step1",
            rx.text("请输入微信读书的cookie"),
            rx.input(
                value= WereadStepState.step_data.get("cookie", ""),
                on_change= WereadStepState.save_step_data("cookie", rx.event.target.value),
            ),
        ),
        rx.cond(
            WereadStepState.current_step == "step2",
            rx.text("请输入notion的token和page_id"),
            rx.text("请先绑定notion，然后复制获得的token和pageid"),
            rx.link(
                "获取token和page_id",
                href="https://api.notion.com/v1/oauth/authorize?client_id=1fad872b-594c-8143-9186-003750ff3168&response_type=code&owner=user&redirect_uri=https%3A%2F%2Fapi.dggpt.top%2Fapi%2Fget_token",
            ),
            rx.input(
                value= WereadStepState.step_data.get("token", ""),
                on_change= WereadStepState.save_step_data("token", rx.event.target.value),
            ),
            rx.input(
                value= WereadStepState.step_data.get("page_id", ""),
                on_change= WereadStepState.save_step_data("page_id", rx.event.target.value),
            ),
        ),
        rx.cond(
            WereadStepState.current_step == "step3",
            rx.text("开始同步"),
            rx.button(
                "立即同步",
                on_click=[
                    # 保存数据
                    WereadState.save_data(WereadStepState.step_data),
                    WereadState.run_sync()
                ],
                margin_top="1em",
            ),
            rx.button(
                "自动同步(系统默认会在每天00:00同步数据)",
                on_click=[
                    WereadStepState.save_step_data(step_label, f"{step_label}数据"),
                    WereadStepState.go_to_step(f"step{int(step_label[-1]) + 1}") if step_label != "step2" else None
                ],
                margin_top="1em",
            ),
        ),
        padding="2em"
    )

def weread_process_flow():
    steps = [f"step{i}" for i in range(1, 3)]
    # labels = [f"步骤{i}" for i in range(1, 6)]
    labels = ["获取cookie", "获取token和page_id", "开始同步"]
    return rx.tabs.root(
        rx.tabs.list(
            *[rx.tabs.trigger(label, value=step) for label, step in zip(labels, steps)],
            spacing="2",
        ),
        *[rx.tabs.content(
            step_content(label),
            value=step,
            padding="2em"
        ) for label, step in zip(labels, steps)],
        value=WereadStepState.current_step,
        on_change=WereadStepState.go_to_step,
        default_value="step1",
        orientation="horizontal"
    )