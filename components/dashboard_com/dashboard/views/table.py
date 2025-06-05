import reflex as rx

from ..backend.product import ProductManagerState
from data.shop_data import ProductSchema

from ..backend.table_state import Item, TableState
from ..components.status_badge import status_badge


def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def _show_item(item: Item, index: int) -> rx.Component:
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(item.name),
        rx.table.cell(f"${item.payment}"),
        rx.table.cell(item.date),
        rx.table.cell(status_badge(item.status)),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return (
        rx.hstack(
            rx.text(
                "Page ",
                rx.code(TableState.page_number),
                f" of {TableState.total_pages}",
                justify="end",
            ),
            rx.hstack(
                rx.icon_button(
                    rx.icon("chevrons-left", size=18),
                    on_click=TableState.first_page,
                    opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-left", size=18),
                    on_click=TableState.prev_page,
                    opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                    color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevron-right", size=18),
                    on_click=TableState.next_page,
                    opacity=rx.cond(
                        TableState.page_number == TableState.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        TableState.page_number == TableState.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                rx.icon_button(
                    rx.icon("chevrons-right", size=18),
                    on_click=TableState.last_page,
                    opacity=rx.cond(
                        TableState.page_number == TableState.total_pages, 0.6, 1
                    ),
                    color_scheme=rx.cond(
                        TableState.page_number == TableState.total_pages,
                        "gray",
                        "accent",
                    ),
                    variant="soft",
                ),
                align="center",
                spacing="2",
                justify="end",
            ),
            spacing="5",
            margin_top="1em",
            align="center",
            width="100%",
            justify="end",
        ),
    )


def main_table() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.flex(
                rx.cond(
                    TableState.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=TableState.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=TableState.toggle_sort,
                    ),
                ),
                rx.select(
                    [
                        "name",
                        "payment",
                        "date",
                        "status",
                    ],
                    placeholder="Sort By: Name",
                    size="3",
                    on_change=TableState.set_sort_value,
                ),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=TableState.setvar("search_value", ""),
                        display=rx.cond(TableState.search_value, "flex", "none"),
                    ),
                    value=TableState.search_value,
                    placeholder="Search here...",
                    size="3",
                    max_width=["150px", "150px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=TableState.set_search_value,
                ),
                align="center",
                justify="end",
                spacing="3",
            ),
            rx.button(
                rx.icon("arrow-down-to-line", size=20),
                "Export",
                size="3",
                variant="surface",
                display=["none", "none", "none", "flex"],
                on_click=rx.download(url="/items.csv"),
            ),
            spacing="3",
            justify="between",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Name", "user"),
                    _header_cell("Payment", "dollar-sign"),
                    _header_cell("Date", "calendar"),
                    _header_cell("Status", "notebook-pen"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    TableState.get_current_page,
                    lambda item, index: _show_item(item, index),
                )
            ),
            variant="surface",
            size="3",
            width="100%",
        ),
        _pagination_view(),
        width="100%",
    )

def _show_product_item(item: ProductSchema, index: int) -> rx.Component:
    
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(item.name),
        rx.table.cell(f"${item.price}"),
        rx.table.cell(item.discount),
        rx.table.cell(item.type),
        rx.table.cell(
            rx.hstack(
                rx.button(
                    rx.icon("edit", size=18),
                    on_click=ProductManagerState.edit_product(item.product_id),
                ),
                rx.button(
                    rx.icon("trash", size=18),
                    on_click=ProductManagerState.delete_product(item.product_id),
                )
            )
        ),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )

def product_table() -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                _header_cell("产品名称", "user"),
                _header_cell("产品价格", "dollar-sign"),
                _header_cell("产品折扣", "calendar"),
                _header_cell("产品类型", "notebook-pen"),
            ),
        ),
        rx.table.body(
            rx.foreach(
                ProductManagerState.product_list,
                lambda item, index: _show_product_item(item, index),
            )
        ),
        variant="surface",
        size="3",
        width="100%",           
    )
def product_modal():
    return rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("添加产品"),
                rx.dialog.description("请填写产品信息"),
                add_product(),
                rx.flex(
                    rx.cond(
                        ProductManagerState.is_edit,
                        rx.button("编辑", on_click=ProductManagerState.update_product),
                        rx.button("添加", on_click=ProductManagerState.add_product),
                    ),
                    rx.dialog.close(
                        rx.button("关闭")
                    ),
                    spacing="3",
                    justify="end",
                ),
                max_width="450px",
            ),
            open=ProductManagerState.is_add,
            on_open_change=ProductManagerState.toggle_add,
    )

def add_product() -> rx.Component:
    
    return rx.flex(
                # 点击加号上传图片，点击图片再次上传图片，上传好显示图片内容
                rx.cond(
                    ProductManagerState.product.image,
                    rx.image(src=rx.get_upload_url(ProductManagerState.product.image),width="100px",height="100px", on_click=ProductManagerState.clear_uploaded_images),
                    rx.upload(
                        rx.box(
                            rx.icon(
                                tag="cloud_upload",
                                style={
                                    "width": "3rem",
                                    "height": "3rem",
                                    "color": "#2563eb",
                                    "marginBottom": "0.75rem",
                                },
                            ),
                            rx.text(
                                "点击上传",
                                style={
                                    "fontWeight": "bold",
                                    "color": "#1d4ed8",
                                },
                            ),
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "padding": "1.5rem",
                                "textAlign": "center",
                            },
                        ),
                        id="product_image_upload",
                        accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]},
                        max_files=1,
                        border="1px dotted #6b7280",
                        padding="2em",
                        on_drop=ProductManagerState.handle_upload(
                            rx.upload_files(upload_id="product_image_upload")
                        ),

                    ),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="产品名称",
                    value=ProductManagerState.product.name,
                    on_change=ProductManagerState.set_product_property("name"),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="说明",
                    value=ProductManagerState.product.description ,
                    on_change=ProductManagerState.set_product_property("description"),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="产品价格",
                    type="number",
                    value=ProductManagerState.product.price ,
                    on_change=ProductManagerState.set_product_property("price"),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="产品折扣",
                    type="number",
                    value=ProductManagerState.product.discount,
                    on_change=ProductManagerState.set_product_property("discount"),
                ),
                rx.input(
                    rx.input.slot(rx.icon("user")),
                    placeholder="产品类型，微信读书为1，kindle为2",
                    type="number",
                    value=ProductManagerState.product.type,
                    on_change=ProductManagerState.set_product_property("type"),
                ),
                spacing="3",
                direction="column",
                align="center",
                width="100%",
                padding="1rem",
            )
