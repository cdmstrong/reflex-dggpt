import datetime
import random

import reflex as rx
from reflex.components.radix.themes.base import (
    LiteralAccentColor,
)
from sqlmodel import select

from Model.User import User
from Model.Vip import Vip
from data.user_data import UserLogin
from data.vip_data import VipSchema


class StatsState(rx.State):
    area_toggle: bool = True
    selected_tab: str = "users"
    timeframe: str = "Monthly"
    users_data = []
    revenue_data = []
    orders_data = []
    device_data = []
    yearly_device_data = []
    pre_users_data = []
    pre_revenue_data = []
    # 表格展示数据
    chart_revenue_data = []
    chart_pre_revenue_data = []
    chart_order_data = []

    chart_pre_order_data = []
    chart_user_data = []
    chart_pre_user_data = []
    is_init = False
    @rx.var
    def user_count(self) -> int:
        # 计算总人数
        return len(self.users_data)

    @rx.var
    def revenue_count(self) -> float:
        # 计算总人数
        count = 0 
        for item in self.revenue_data:
            count += item.vip_price
        return count
    
    @rx.var
    def order_count(self) -> int:
        # 计算总人数
        return len(self.revenue_data)
    
    @rx.var
    def pre_user_count(self) -> int:
        # 计算总人数
        return len(self.pre_users_data)

    @rx.var
    def pre_revenue_count(self) -> float:
        # 计算总人数
        count = 0 
        for item in self.pre_revenue_data:
            count += item.vip_price
        return count
    
    @rx.var
    def pre_order_count(self) -> int:
        # 计算总人数
        return len(self.pre_revenue_data)
    
    @rx.event
    def set_selected_tab(self, tab: str | list[str]):
        self.selected_tab = tab if isinstance(tab, str) else tab[0]
    def toggle_areachart(self):
        self.area_toggle = not self.area_toggle

    def get_data(self):
        cur_data = datetime.datetime.now() - datetime.timedelta(days=30)
        end_data = datetime.datetime.now()
        self.users_data = self.get_user_data(cur_data, end_data)
        self.revenue_data = self.get_revenue_data(cur_data, end_data)
        self.get_pre_data()
        self.randomize_data()

    # 获取前30日数据
    def get_pre_data(self):
        cur_data = datetime.datetime.now() - datetime.timedelta(days=60)
        end_data = datetime.datetime.now() - datetime.timedelta(days=30)
        self.pre_users_data = self.get_user_data(cur_data, end_data)
        self.pre_revenue_data = self.get_revenue_data(cur_data, end_data)

    def get_user_data(self, start_time: datetime, end_time: datetime) -> list[UserLogin]:
        print(start_time, end_time)
        # 查询数据库，并返回数据
        with rx.session() as session:
            statement = select(User).where(
                User.register_time.between(start_time, end_time)
            )
            result = session.exec(statement)
            user_list = result.all()
            return [UserLogin.from_orm(user) for user in user_list]

    def get_revenue_data(self, start_time: datetime, end_time: datetime) -> list[VipSchema]:
        # 查询数据库，并返回数据
        with rx.session() as session:
            statement = select(Vip).where(
                Vip.start_time.between(start_time, end_time)
            )
            result = session.exec(statement)
            vip_list = result.all()
            return [VipSchema.from_orm(vip) for vip in vip_list]
    

    def randomize_data(self):
        # If data is already populated, don't randomize
        if self.is_init:
            return

        for i in range(30, -1, -1):  # Include today's data
            day = datetime.datetime.now() - datetime.timedelta(days=i)
            pre_day = datetime.datetime.now() - datetime.timedelta(days=30) - datetime.timedelta(days=i)
            # 获取revenue_data的所有register_time等于day的数据，如果没有输入0，只要年月日相同就行
            revenue_data = [item for item in self.revenue_data if item.register_time.date() == day.date()]
            if revenue_data:
                revenue = sum([item.vip_price for item in revenue_data])
            else:
                revenue = 0

            pre_revenue_data = [item for item in self.pre_revenue_data if item.register_time.date() == pre_day.date()]
            if pre_revenue_data:
                pre_revenue = sum([item.vip_price for item in pre_revenue_data])
            else:
                pre_revenue = 0
            self.chart_revenue_data.append(
                    {
                        "Date": day.strftime("%m-%d"),
                        "Revenue": 0 if not revenue_data else revenue
                    }
            )
            self.chart_pre_revenue_data.append(
                {
                    "Date": pre_day.strftime("%m-%d"),
                    "Revenue": 0 if not pre_revenue_data else pre_revenue
                }
            )
            # 获取订单数
            order_data = [item for item in self.orders_data if item.register_time.date() == day.date()]
            pre_order_data = [item for item in self.pre_revenue_data if item.register_time.date() == pre_day.date()]

            self.chart_order_data.append(
                {
                    "Date": day.strftime("%m-%d"),
                    "Orders": 0 if not order_data else len(order_data)
                    
                }
            )
            self.chart_pre_order_data.append(
                {
                    "Date": pre_day.strftime("%m-%d"),
                    "Orders": 0 if not pre_order_data else len(pre_order_data)
                }
            )
            # 获取用户数
            user_data = [item for item in self.users_data if item.register_time.date() == day.date()]
            pre_user_data = [item for item in self.pre_users_data if item.register_time.date() == pre_day.date()]
           
            self.chart_user_data.append(
                {
                    "Date": day.strftime("%m-%d"),
                    "Users": 0 if not user_data else len(user_data)
                    
                }
            )
            self.chart_pre_user_data.append(
                {
                    "Date": pre_day.strftime("%m-%d"),
                    "Users": 0 if not pre_user_data else len(pre_user_data)
                }
            )
        print(f"pre_user_data: {self.chart_pre_revenue_data}")
        print(f"pre_user_data: {self.chart_pre_order_data}")
        print(f"pre_user_data: {self.chart_pre_user_data}")
        self.is_init = True
        self.device_data = [
            {"name": "Desktop", "value": 23, "fill": "var(--blue-8)"},
            {"name": "Mobile", "value": 47, "fill": "var(--green-8)"},
            {"name": "Tablet", "value": 25, "fill": "var(--purple-8)"},
            {"name": "Other", "value": 5, "fill": "var(--red-8)"},
        ]

        self.yearly_device_data = [
            {"name": "Desktop", "value": 34, "fill": "var(--blue-8)"},
            {"name": "Mobile", "value": 46, "fill": "var(--green-8)"},
            {"name": "Tablet", "value": 21, "fill": "var(--purple-8)"},
            {"name": "Other", "value": 9, "fill": "var(--red-8)"},
        ]


def area_toggle() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.icon_button(
            rx.icon("area-chart"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=StatsState.toggle_areachart,
        ),
        rx.icon_button(
            rx.icon("bar-chart-3"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=StatsState.toggle_areachart,
        ),
    )


def _create_gradient(color: LiteralAccentColor, id: str) -> rx.Component:
    return (
        rx.el.svg.defs(
            rx.el.svg.linear_gradient(
                rx.el.svg.stop(
                    stop_color=rx.color(color, 7), offset="5%", stop_opacity=0.8
                ),
                rx.el.svg.stop(
                    stop_color=rx.color(color, 7), offset="95%", stop_opacity=0
                ),
                x1=0,
                x2=0,
                y1=0,
                y2=1,
                id=id,
            ),
        ),
    )


def _custom_tooltip(color: LiteralAccentColor) -> rx.Component:
    return (
        rx.recharts.graphing_tooltip(
            separator=" : ",
            content_style={
                "backgroundColor": rx.color("gray", 1),
                "borderRadius": "var(--radius-2)",
                "borderWidth": "1px",
                "borderColor": rx.color(color, 7),
                "padding": "0.5rem",
                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
            },
            is_animation_active=True,
        ),
    )


def users_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("blue", "colorBlue"),
            _custom_tooltip("blue"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Users",
                stroke=rx.color("blue", 9),
                fill="url(#colorBlue)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.chart_pre_user_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            _custom_tooltip("blue"),
            rx.recharts.bar(
                data_key="Users",
                stroke=rx.color("blue", 9),
                fill=rx.color("blue", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.chart_user_data,
            height=425,
        ),
    )


def revenue_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("green", "colorGreen"),
            _custom_tooltip("green"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Revenue",
                stroke=rx.color("green", 9),
                fill="url(#colorGreen)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.chart_revenue_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            _custom_tooltip("green"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="Revenue",
                stroke=rx.color("green", 9),
                fill=rx.color("green", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.chart_pre_revenue_data,
            height=425,
        ),
    )


def orders_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("purple", "colorPurple"),
            _custom_tooltip("purple"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Orders",
                stroke=rx.color("purple", 9),
                fill="url(#colorPurple)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.chart_order_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            _custom_tooltip("purple"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="Orders",
                stroke=rx.color("purple", 9),
                fill=rx.color("purple", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.chart_pre_order_data,
            height=425,
        ),
    )


def pie_chart() -> rx.Component:
    return rx.cond(
        StatsState.timeframe == "Yearly",
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=StatsState.yearly_device_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=StatsState.device_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        ),
    )


def timeframe_select() -> rx.Component:
    return rx.select(
        ["Monthly", "Yearly"],
        default_value="Monthly",
        value=StatsState.timeframe,
        variant="surface",
        on_change=StatsState.set_timeframe,
    )
