from functools import partial

from nicegui import ui, app

from dorky import assets_dir


async def check(port: int) -> None:
    """Check if pop-ups are allowed in the browser and show a warning dialog if not."""
    async def popup_state() -> bool:
        """Check if pop-ups are allowed in the browser by opening a small blank popup."""
        is_allowed = await ui.run_javascript(
            f"""
            (() => {{
                const p = window.open('http://127.0.0.1:{port}/popup', '', 'width=300,height=150');
                if (!p) return false;
                p.close();
                return true;
            }})()
            """,
            timeout=15,
        )
        return is_allowed

    # Does thee popup state has been checked before?
    popup_allowed = app.storage.user.get("popup_allowed")
    # Does the alert for the user has been already shown?
    view_warning = app.storage.user.get("view_warning")
    # Check as sessions do expire
    if not popup_allowed and view_warning:
        # Get the browser popup state
        popup_state = await popup_state()
        # If popups are allowed, update the storage
        if popup_state:
            app.storage.user.update(popup_allowed=True)
            app.storage.user.update(view_warning=False)
        else:
            # Show the warning dialog if pop-ups are not allowed
            with ui.dialog() as dialog, ui.card():
                # Do not show the warning again
                app.storage.user.update(view_warning=False)
                with ui.row().style():
                    ui.image(assets_dir + "/images/dorky-head.png").style(
                        "width: 30px; height: 30px; margin: 0px; padding: 0px;"
                    ).props("fit=contain")
                    ui.label("Allow pop-ups for dorky domain").classes("text-h6")
                ui.label(
                    "Pop-up windows should be allowed for Dorky website to work properly."
                )
                with ui.row().style(
                    "width: 100%; display: flex; align-items: center; justify-content: space-between;"
                ):
                    ui.link("Get some help", "https://support.mozilla.org/en-US/kb/pop-blocker-settings-exceptions-troubleshooting#w_what-are-pop-ups", new_tab=True)
                    ui.button("Close", on_click=dialog.close)

            # Show the dialog
            async def show():
                await dialog

            # Run the dialog only once without user interaction
            ui.timer(0, partial(show), once=True)
