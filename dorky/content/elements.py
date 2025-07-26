from nicegui import ui, app

from dorky import assets_dir


class ToggleButton(ui.button):
    """Toggle help and so."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._state = app.storage.user["view_help"]
        self.style("color: #555;")
        self.on("click", self.toggle)

    def toggle(self) -> None:
        """Toggle the button state."""
        self._state = not self._state
        self.update()

    def update(self) -> None:
        self.icon = "arrow_drop_up" if self._state else "arrow_drop_down"
        super().update()


def header() -> None:
    """Header with the Dorky logo and a link to the Firefox Add-on page."""
    with ui.row().style(
        "width: 100%; display: flex; align-items: center; justify-content: space-between"
    ):
        with ui.link("", "/"):
            ui.image(assets_dir + "/images/dorky-logo.png").style(
                "width: 200px; height: 60px; margin: 0px; padding: 0px;"
            ).props("fit=contain")
        with ui.link(
            "", "https://addons.mozilla.org/en-US/firefox/addon/dorky/", new_tab=True
        ):
            ui.image(assets_dir + "/images/addon.png").style(
                "width: 60px; height: 60px; margin: 0px; padding: 0px;"
            ).props("fit=contain")
    with ui.row():
        ui.label("Search and dork across multiple search engines :)")

def footer() -> None:
    """Footer with links to the GitHub repository"""
    with ui.row().style(
        "width: 100%; justify-content: center; margin-top: 20px; flex-direction: row;"
    ):
        with ui.link("", "https://github.com/balestek/dorky-app", new_tab=True):
            ui.image(assets_dir + "/images/github-mark.png").style(
                "height:30px; width:30px;"
            )

# Dorky ASCII art for cli
dorky_ascii = """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠛⠋⠉⠉⠉⠛⠛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠒⠂⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣇⠈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣷⡀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠻⠛⠛⠛⠻⢿⣿⣿⣿
⣿⣿⣿⣷⣶⣶⡶⠂⠀⠀⠀⠀⠀⢀⣠⣴⣶⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣄⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣿⣿⣿
⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⣠⣶⠿⠛⠉⠉⠀⠀⣴⡇⠀⠀⠀⠀⣠⣾⣿⠋⠉⠉⠛⢿⡆⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿
⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⣴⣿⣋⣤⣴⣶⣶⣄⢠⣿⣇⠀⠀⠀⣾⣿⣿⣿⣤⣤⣤⣤⣄⣹⣄⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿
⣿⣿⣧⣴⣾⠀⠀⠀⠀⣸⠿⠋⠉⠀⠀⠀⠈⠉⠻⣿⣿⡄⠀⢸⣿⣿⡿⠟⢉⣁⡤⠤⣄⣉⠙⠦⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿
⣿⣿⣿⣿⡇⠀⠀⠀⠀⠁⠀⠀⣀⣤⣤⣤⣄⡀⠂⠀⠻⣿⣤⣼⣿⠏⢠⠖⢉⣠⣤⣤⣤⣈⠑⢦⠀⠀⠀⠀⠀⣷⣄⣽⣿⣿
⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⢠⡾⢉⣤⣤⡄⠈⠻⣆⠀⠀⠹⠿⠿⠏⢰⠃⣴⣿⣿⣿⣿⣿⣿⣷⡄⢳⠀⠀⠀⠀⢸⣿⣿⣿⣿
⣿⣿⣿⣿⡇⠀⠤⠄⠀⠀⣾⢀⣿⠟⠿⠇⠀⠀⢹⠀⠀⠀⠒⠒⠀⡎⢰⡿⠛⠉⣀⣀⣈⠉⠻⣷⠈⡆⠠⠤⠀⢸⣿⣿⣿⣿
⣿⣿⠟⠋⠁⠀⠀⠀⠀⠀⢻⡌⣿⣆⠀⠀⠀⣀⣾⠀⠀⢠⣶⣶⡄⢡⠈⣷⣿⣿⣿⣿⣿⣿⣷⠏⢰⠁⠀⠀⠀⠈⠙⠻⣿⣿
⣿⠃⢠⣾⠿⢿⣷⡄⠀⠀⠀⠙⢿⣿⣿⣿⣿⠟⠁⠀⢀⣾⣿⣿⣧⡀⢣⡈⠻⣿⣿⣿⣿⡿⠋⡠⠃⠀⢀⣾⡿⠿⣷⡄⠘⣿
⡇⠀⣿⢁⣴⡤⠘⡇⠸⣦⣀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣷⣄⡙⠲⠤⣤⣡⡤⠴⠊⣀⣾⠇⢸⠋⢤⣦⡈⣿⠀⢹
⣧⠀⢿⣼⣿⠁⣴⣇⠀⣿⣿⡷⠖⠀⢠⣤⣴⣶⣿⣿⡏⠉⢿⡿⠋⢙⣿⣿⣶⣦⣤⡄⠀⠒⢾⣿⣿⠀⣼⣦⠈⣿⣧⡿⠀⣼
⣿⣆⠈⠻⣿⣧⣈⣻⡀⢹⡿⢀⡀⢈⠙⠻⢿⣿⣿⣿⣿⣦⣾⣷⣶⣿⣿⣿⣿⡿⠿⠛⣁⢀⡀⢻⡇⢀⣟⣁⣴⣿⠟⠁⣰⣿
⣿⣿⣷⣄⡈⠉⠛⠛⠁⠀⢿⣿⣧⠈⠋⠰⣦⠀⣉⡉⠛⠛⠛⠛⠛⠛⠉⣉⠁⣤⡦⠘⠁⣼⣷⡿⠀⠈⠙⠛⠉⢁⣠⣾⣿⣿
⣿⣿⣿⣿⣿⣿⣷⣶⣿⣆⠈⢿⣿⣧⡀⠢⡌⠀⠛⠏⢸⣿⡇⢸⣿⡇⠸⠟⠃⢀⡴⢀⣼⣿⡿⠁⣰⣿⣿⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠈⠻⣿⣿⣦⡀⠛⠿⠆⣴⣤⡄⢠⣤⣤⠀⡾⠟⢀⣠⣾⣿⠟⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠙⢿⣿⣿⣷⣦⣤⣈⣉⣁⣈⣉⣉⣠⣴⣶⣿⣿⡿⠃⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠉⠻⣿⣿⣿⣿⣿⡟⢛⣿⣿⣿⣿⣿⠟⠁⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠉⠛⠿⢿⣿⣿⡿⠿⠛⠉⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣀⣀⣠⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                                by jm balestek
"""