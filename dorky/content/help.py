from nicegui import ui, app

from dorky.content import elements


def help_block() -> None:
    help_style = "border-radius: 50%; background-color: #c2c2c2; color: white; width: 20px; height: 20px; text-align: center; margin-right: 7px;"

    elements.ToggleButton("Help", color="#e6e6e6").on_click(
        lambda: app.storage.user.update(
            view_help=False if app.storage.user["view_help"] is True else True
        )
    )

    with ui.column().bind_visibility_from(app.storage.user, "view_help"):
        with ui.list().props("dense").style("color: #555;"):
            with ui.item():
                ui.label("1").style(help_style)
                ui.label(
                    "Authorize pop-up windows for Dorky website in your browser settings."
                )
            with ui.item():
                ui.label("2").style(help_style)
                ui.label("Choose the search engines. Highlighted = active.")
            with ui.item():
                ui.label("3").style(help_style)
                ui.label("Write your search query.")
            with ui.item():
                ui.label("4").style(help_style)
                ui.label("Press Enter or click the search button.")
