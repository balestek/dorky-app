import os
import uuid

from fastapi import Header, Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, PlainTextResponse
from nicegui import ui, app, Client
from nicegui.events import GenericEventArguments

from dorky import assets_dir
from dorky.content import operators, help, popup, elements
from dorky.search_engines import Search


def main(port: int):
    # Load the serach engines
    engines_list = ["Google", "Bing", "Yandex", "DuckDuckGo", "Brave", "Baidu"]
    # Assets declaration
    app.add_static_files("assets", assets_dir)

    # Startup message
    app.on_startup(lambda: print(f"{elements.dorky_ascii}\n🚀 Dorky is up and running 🚀\n\n"
                                 f"🌐 Visit http://127.0.0.1:{port} or http://localhost:{port}.\n\n"
                                 f"🛑 Press Ctrl+C to stop Dorky."))

    # Main page
    @ui.page("/", title="Dorky search")
    async def search_page():
        """Main page of Dorky."""
        await ui.context.client.connected(timeout=10)

        # Set default storage values
        for key, default in [
            ("search", ""),
            ("popup_allowed", False),
            ("view_warning", True),
            ("view_help", True),
            ("view_operators", True),
            ("Google", True),
            ("Bing", True),
            ("Yandex", True),
            ("DuckDuckGo", False),
            ("Brave", False),
            ("Baidu", False)
        ]:
            app.storage.user.setdefault(key, default)

        # Add the header
        elements.header()

        # Add the search engines buttons
        with ui.row():
            def create_browser_button(engine_name):
                """Create a button for each search engine_name."""
                with ui.row().style("cursor: pointer;").style(
                        "filter: grayscale(0%);"
                        if app.storage.user[engine_name]
                        else "filter: grayscale(100%);"
                ).on("click", lambda e: image_change(e, engine_name)):
                    ui.image(assets_dir + f"/images/{engine_name.lower()}.png").style(
                        "width: 20px; height: 20px; margin: 0px; padding: 0px; "
                    )
                    ui.label(engine_name).style("color: #0060df; margin: 0 0 0 -10px;")

            for engine in engines_list:
                create_browser_button(engine)

        def trim_search_value(e: GenericEventArguments) -> None:
            """Trim the search input value to remove the new line induced by hitting Enter."""
            if e.sender.value:
                e.sender.value = e.sender.value.strip()

        def _enter_down(e: GenericEventArguments) -> None:
            """Handle the Enter key down event to run the search."""
            e.sender.clear()
            trim_search_value(e)
            run_search()

        # Add the search input and button
        with ui.row().style("width:100%"):
            ui.input(placeholder="Type your search").style("width:80%").props(
                "outlined dense clearable width=100% autogrow"
            ).bind_value(app.storage.user, "search").on("keydown.enter", _enter_down)

            ui.button("Search").on_click(
                run_search
            )

        # Add the help block
        with ui.column():
            help.help_block()
        # Add the operators table
        with ui.row():
            operators.operators_table()
        # Add the footer
        elements.footer()

        # Check if the pop-ups are allowed in the browser
        await popup.check(port)

    # Add the CORS header for the API endpoint cerating a FastAPI sub app
    api_app = app

    api_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["X-Dorky"]
    )

    # Create the API endpoint to use with the extension
    @api_app.get("/api/")
    def api_get_converted_urls(engines: str = "", search: str = "", source: str = "", x_dorky: str = Header(None)) -> JSONResponse or RedirectResponse:
        """API endpoint for the ff addon to convert the search query to URLs."""
        if x_dorky is None:
            return RedirectResponse(url="/")
        # Return an error if the search is empty
        if search == "":
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error"
                },
            )
        # Convert the search query to URLs using the selected engines
        engines = engines.split(",")
        result = Search(search, engines).convert()
        if result["status"] == "ok":
            # Reverse the URLs as the add-on behaviour is different from the web app when opening the tabs
            result["urls"].reverse()

        return JSONResponse(content=result)

    @ui.page("/popup", title="Dorky Popup Check")
    def popup_check_page():
        """Popup check page for Dorky."""
        ui.label("Popup check page for Dorky.").style("text-align: center; margin-top: 20px;")
        ui.label("You can close this window.").style("text-align: center; margin-top: 10px;")

    # Toggle the grayscale filter for the chosen search engine images
    def image_change(e: GenericEventArguments, engine: str) -> None:
        """Toggle the grayscale filter for the chosen search engine images."""
        if app.storage.user[engine]:
            app.storage.user[engine] = False
            e.sender.style("filter: grayscale(100%)")
        else:
            app.storage.user[engine] = True
            e.sender.style("filter: grayscale(0%)")

    def run_search() -> None:
        """Run the convertor with the selected engines and open tabs."""
        if not app.storage.user["search"] or app.storage.user["search"].strip() == "":
            ui.notify("Fill the search input with your query.", position="center", type="negative", close_button=True)
            return
        engines = [
            key
            for key, value in app.storage.user.items()
            if value and key in engines_list
        ]
        if not engines:
            ui.notify("No search engines selected. Please select at least one engine.", position="center", type="negative", close_button=True)
            return
        search_urls = Search(app.storage.user["search"], engines).convert()
        if search_urls["status"] == "error":
            ui.notify(search_urls["error"], position="center", type="negative", close_button=True)
        else:
            for url in search_urls["urls"]:
                ui.navigate.to(url, new_tab=True)

    @app.exception_handler(404)
    async def not_found_exception_handler(request: Request, exc: HTTPException) -> RedirectResponse:
        """Handle 404 errors by redirecting to the main page."""
        return RedirectResponse("/")

    @app.exception_handler(500)
    async def not_found_exception_handler(request: Request, exc: HTTPException) -> None:
        return

    @app.get("/robots.txt", response_class=PlainTextResponse)
    def robots() -> str:
        """Serve the robots.txt file."""
        with open(assets_dir + "/robots.txt", "r") as file:
            return file.read()

    # Check if the storage secret is set with the env variable;
    # if not, delete the storage and set a new secret.
    if secret := os.getenv("DORKY_SECRET"):
        print(f"🔑 Using DORKY_SECRET from environment for storage.")
    else:
        app.storage.clear()
        print(f"🗑️DORKY_SECRET not found, storage deleted.")
        secret = str(uuid.uuid4())
        print(f"🔑 New secret generated for storage.")

    # Run the app
    ui.run(
        port=port,
        storage_secret=secret,
        show=False,
        reload=False,
        show_welcome_message=False,
        favicon=assets_dir + "/images/favicon.ico",
    )
