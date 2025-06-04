from calendar import day_name
import reflex as rx
from reflex.components.radix.themes.base import LiteralAccentColor

from components.dashboard_com.dashboard.views.charts import StatsState

from .. import styles


def stats_card(
    stat_name: str,
    value: int,
    prev_value: int,
    icon: str,
    icon_color: LiteralAccentColor,
    extra_char: str = "",
) -> rx.Component:
    percentage_change = rx.cond(
        prev_value != 0,
        round(((value - prev_value) /prev_value) * 100, 2),
        rx.cond(
            value == 0,
            0,
            float("inf")
        )
    )

    change = rx.cond(
        value > prev_value,
        "increase",
        "decrease"
    )

    arrow_icon = rx.cond(
        value > prev_value,
        "trending-up",
        "trending-down"
    )

    arrow_color = rx.cond(
        value > prev_value,
        "grass",
        "tomato"
    )
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(tag=icon, size=34),
                    color_scheme=icon_color,
                    radius="full",
                    padding="0.7rem",
                ),
                rx.vstack(
                    rx.heading(
                        f"{extra_char}{value:,}",
                        size="6",
                        weight="bold",
                    ),
                    rx.text(stat_name, size="4", weight="medium"),
                    spacing="1",
                    height="100%",
                    align_items="start",
                    width="100%",
                ),
                height="100%",
                spacing="4",
                align="center",
                width="100%",
            ),
            rx.hstack(
                rx.hstack(
                    rx.icon(
                        tag=arrow_icon,
                        size=24,
                        color=rx.color(arrow_color, 9),
                    ),
                    rx.text(
                        f"{percentage_change}%",
                        size="3",
                        color=rx.color(arrow_color, 9),
                        weight="medium",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.text(
                    f"{change} from last month",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                align="center",
                width="100%",
            ),
            spacing="3",
        ),
        size="3",
        width="100%",
        box_shadow=styles.box_shadow_style,
    )


def stats_cards() -> rx.Component:
    return rx.grid(
        stats_card(
            stat_name="用户数",
            value=StatsState.user_count,
            prev_value=StatsState.pre_user_count,
            icon="users",
            icon_color="blue",
        ),
        stats_card(
            stat_name="充值金额",
            value=StatsState.revenue_count,
            prev_value=StatsState.pre_revenue_count,
            icon="dollar-sign",
            icon_color="green",
            extra_char="$",
        ),
        stats_card(
            stat_name="订单数",
            value=StatsState.order_count,
            prev_value=StatsState.pre_order_count,
            icon="shopping-cart",
            icon_color="purple",
        ),
        gap="1rem",
        grid_template_columns=[
            "1fr",
            "repeat(1, 1fr)",
            "repeat(2, 1fr)",
            "repeat(3, 1fr)",
            "repeat(3, 1fr)",
        ],
        width="100%",
    )
