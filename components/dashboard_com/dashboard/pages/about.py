"""The about page."""

from pathlib import Path

import reflex as rx

from .. import styles
from ..templates import template
from services.login_service import LoginState


@template(route="/about", title="About")
def about() -> rx.Component:
    """The about page.

    Returns:
        The UI for the about page.
    """
    with Path("about.md").open(encoding="utf-8") as readme:
        content = readme.read()
    return rx.markdown(content, component_map=styles.markdown_style)
