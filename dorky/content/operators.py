from nicegui import ui, app

from dorky.content import elements

operator_list = [
    {
        "table": {
            "operator": '" "',
            "name": "Quotation marks",
            "native": "yes",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "yes",
            "brave": "yes",
            "baidu": "yes",
        },
        "operator": '" "',
        "name": "Quotations marks",
        "description": "Results that mention an exact word or phrase",
        "examples": [
            {
                "example": '"trace labs global"',
                "explanation": "Results containing the exact phrase <code>trace labs global</code>.",
            }
        ],
    },
    {
        "table": {
            "operator": "( )",
            "name": "Parentheses",
            "native": "yes",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "yes",
            "brave": "yes",
            "baidu": "yes",
        },
        "description": "Group multiple operators",
        "examples": [
            {
                "example": "osint AND (geoint OR socmint)",
                "explanation": "Results containing <code>osint</code> and either <code>geoint</code> or <code>socmint</code>.",
            }
        ],
    },
    {
        "table": {
            "operator": "OR, |",
            "name": "OR operator",
            "native": "yes",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "yes",
            "brave": "yes",
            "baidu": "yes",
        },
        "description": "Search for X or Y",
        "examples": [
            {
                "example": "osint OR geoint",
                "explanation": "Results containing either <code>osint</code> or <code>geoint</code>.",
            },
            {
                "example": "osint | geoint",
                "explanation": "Results containing either <code>osint</code> or <code>geoint</code>.",
            },
        ],
    },
    {
        "table": {
            "operator": "AND",
            "name": "AND operator",
            "native": "yes",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "yes",
            "brave": "yes",
            "baidu": "yes",
        },
        "description": "Search for X and Y",
        "examples": [
            {
                "example": "osint AND geoint",
                "explanation": "Results containing both <code>osint</code> and <code>geoint</code>.",
            }
        ],
    },
    {
        "table": {
            "operator": "-",
            "name": "Exclude operator",
            "native": "yes",
            "google": "yes",
            "bing": "yes",
            "yandex": "partial",
            "duckduckgo": "yes",
            "brave": "partial",
            "baidu": "partial",
        },
        "description": "Search without including a specific term.",
        "examples": [
            {
                "example": "osint -geoint",
                "explanation": "Results containing <code>osint</code> but not <code>geoint</code>.",
            },
            {
                "example": "osint -site:github.com",
                "explanation": "Results containing <code>osint</code> but excluding those from <code>github.com</code>.",
            },
        ],
        "notes": [
            {
                "engine": "yandex",
                "note": "Works only with a single word, not with operators. The operator and its value are removed.",
            },
            {
                "engine": "brave",
                "note": "Works only with a single word, not with operators. The operator and its value are removed.",
            },
            {
                "engine": "baidu",
                "note": "Works only with a single word, not with operators. The operator and its value are removed.",
            },
        ],
    },
    {
        "table": {
            "operator": "site:",
            "name": "Site search",
            "native": "yes",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "yes",
            "brave": "yes",
            "baidu": "yes",
        },
        "description": "Search within a specific website",
        "examples": [
            {
                "example": "osint site:github.com",
                "explanation": "Results containing <code>osint</code> from <code>github.com</code>.",
            }
        ],
    },
    {
        "table": {
            "operator": "inurl:",
            "name": "URL search",
            "native": "yes",
            "google": "yes",
            "bing": "no",
            "yandex": "yes",
            "duckduckgo": "yes",
            "brave": "yes",
            "baidu": "yes",
        },
        "description": "Search for a word in the URL",
        "examples": [
            {
                "example": "osint inurl:usa",
                "explanation": "Results containing <code>osint</code> and the word <code>usa</code> in the URL.",
            }
        ],
        "notes": [
            {
                "engine": "bing",
                "note": "No equivalent exists; the operator is removed from the search query, but its value is retained.",
            }
        ],
    },
    {
        "table": {
            "operator": "intitle:",
            "name": "Title search",
            "native": "yes",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "yes",
            "brave": "yes",
            "baidu": "yes",
        },
        "description": "Search for a word in the title",
        "examples": [
            {
                "example": "olympic games intitle:osint",
                "explanation": "Results with <code>olympic games</code> and <code>osint</code> in the title.",
            }
        ],
    },
    {
        "table": {
            "operator": "intext:",
            "name": "Text search",
            "native": "yes",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "no",
            "brave": "yes",
            "baidu": "no",
        },
        "description": "Search for a word in the text or body",
        "examples": [
            {
                "example": "osint intext:tools",
                "explanation": "Results containing both <code>osint</code> and <code>tools</code> in the text.",
            }
        ],
        # TODO: Maybe replacing intext with + or "" ?
        "notes": [
            {
                "engine": "duckduckgo",
                "note": "No equivalent exists; the operator is removed from the search query, but its value is retained.",
            },
            {
                "engine": "baidu",
                "note": "No equivalent exists; the operator is removed from the search query, but its value is retained.",
            },
        ],
    },
    {
        "table": {
            "operator": "filetype:, ext:",
            "name": "File search",
            "native": "yes",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "yes",
            "brave": "yes",
            "baidu": "yes",
        },
        "description": "Search for a specific file type",
        "examples": [
            {
                "example": "osint filetype:pdf",
                "explanation": "Results containing <code>osint</code> in PDF format.",
            },
            {
                "example": "osint ext:pdf",
                "explanation": "Results containing <code>osint</code> in PDF format.",
            },
        ],
    },
    {
        "table": {
            "operator": "*",
            "name": "Wildcard search",
            "native": "yes",
            "google": "yes",
            "bing": "no",
            "yandex": "yes",
            "duckduckgo": "no",
            "brave": "no",
            "baidu": "no",
        },
        # TODO: Check if it's working in other operators like site, intext,...
        "description": 'Search for terms using a wildcard; it only works within <code>""</code>.',
        "examples": [
            {
                "example": '"osint * tools"',
                "explanation": "Results containing <code>osint someword(s) tools</code>.",
            }
        ],
        "notes": [
            {
                "engine": "bing",
                "note": "No equivalent exists; the operator is removed, and the words are placed inside <code>""</code>.",
            },
            {
                "engine": "duckduckgo",
                "note": "No equivalent exists; the operator is removed, and the words are placed inside <code>""</code>.",
            },
            {
                "engine": "brave",
                "note": "No equivalent exists; the operator is removed, and the words are placed inside <code>""</code>.",
            },
            {
                "engine": "baidu",
                "note": "No equivalent exists; the operator is removed, and the words are placed inside <code>""</code>.",
            },
        ],
    },
    {
        "table": {
            "operator": "after:",
            "name": "Date search",
            "native": "yes",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "yes",
            "brave": "yes",
            "baidu": "yes",
        },
        "description": "Search for a term starting from a specific date ",
        "examples": [
            {
                "example": "osint after:2025-01-31",
                "explanation": "Results containing <code>osint</code> from January 31, 2025.",
            }
        ],
    },
    {
        "table": {
            "operator": "before:",
            "name": "Date search",
            "native": "yes",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "yes",
            "brave": "yes",
            "baidu": "yes",
        },
        "description": "Search for a term up to a specific date",
        "examples": [
            {
                "example": "osint before:2024-12-31",
                "explanation": "Results containing <code>osint</code> up to December 31, 2024.",
            }
        ],
    },
    {
        "table": {
            "operator": "lang:",
            "name": "Language search",
            "native": "no",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "no",
            "brave": "partial",
            "baidu": "no",
        },
        "description": "Search in a specific language using <a href='https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes#Table' style='color: #5898d4' target='_blank'>ISO 639-1 language codes</a>.",
        "examples": [
            {
                "example": "osint lang:es",
                "explanation": "Results that contain <code>osint</code> in Spanish.",
            }
        ],
        "notes": [
            {
                "engine": "duckduckgo",
                "note": "Language is filtered by country, so searching in English could require opening 13 windows (e.g., UK, NZ, ZA, CA, etc.). The operator and its value are removed.",
            },
            {
                "engine": "brave",
                "note": "Equivalent exists but results are limited.",
            },
            {
                "engine": "baidu",
                "note": "Only three languages are supported: all languages, Simplified Chinese, and Traditional Chinese. The operator and its value are removed.",
            },
        ],
    },
    {
        "table": {
            "operator": "country:",
            "name": "Country search",
            "native": "no",
            "google": "yes",
            "bing": "yes",
            "yandex": "yes",
            "duckduckgo": "partial",
            "brave": "yes",
            "baidu": "no",
        },
        "description": "Search within a specific country using <a href='https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements' style='color: #5898d4' target='_blank'>ISO 3166-1 alpha-2 country codes</a>.",
        "examples": [
            {
                "example": "osint country:us",
                "explanation": "Search results for <code>osint</code> specific to the United States.",
            }
        ],
        "notes": [
            {
                "engine": "duckduckgo",
                "note": "Country options are limited. If a specific country is unavailable, the search will default to a global scope. Since results are filtered by language per country, Dorky can open multiple windows—for example, both 'fr' and 'nl' for Belgium.",
            },
            {
                "engine": "baidu",
                "note": "There is no equivalent; both the operator and its value are removed.",
            },
        ],
    },
    {
        "table": {
            "operator": "sub:",
            "name": "Subdomain search",
            "native": "no",
            "google": "yes",
            "bing": "no",
            "yandex": "yes",
            "duckduckgo": "no",
            "brave": "no",
            "baidu": "no",
        },
        "description": "Search across subdomains of a domain",
        "examples": [
            {
                "example": "sub:tesla.com incident",
                "explanation": "Results about <code>incident</code> in the subdomains of <code>tesla.com</code>..",
            },
            {
                "example": "sub:tesla.com",
                "explanation": "All <code>tesla.com</code> results found in URLs of its subdomains.",
            },
        ],
        "notes": [
            {
                "note": "This special operator only works with Google and Yandex. It will only launch them despite your search engine choice.",
            },
            {
                "note": "When used without other operators, it can find sub-domains that are referenced by search engines.",
            },
        ],
    },
    {
        "table": {
            "operator": "last:",
            "name": "Last duration search",
            "native": "no",
            "google": "yes",
            "bing": "no",
            "yandex": "no",
            "duckduckgo": "no",
            "brave": "no",
            "baidu": "no"
        },
        "description": "Search results from the last X hours (h), minutes (m), or seconds (s) indexed by Google.",
        "examples": [
            {
                "example": "osint last:1h",
                "explanation": "Results about <code>osint</code> indexed by Google within the last hour.",
            },
            {
                "example": "osint last:5m",
                "explanation": "Results about <code>osint</code> indexed by Google within the last 5 minutes.",
            },
            {
                "example": "osint last:30s",
                "explanation": "Results about <code>osint</code> indexed by Google within the last 30 seconds.",
            }
        ],
        "notes": [
            {
                "note": "This operator is exclusive to Google and will force a Google search, no matter which search engine you use.",
            },
            {
                "note": "It can't be used with <code>before:</code> or <code>after:</code>; both are ignored.",
            },
            {
                "note": "Using minutes or seconds can help monitor a hot topic in real time.",
            }
        ]
    }
]

columns = [
    {"name": "google", "label": "Google", "field": "google"},
    {"name": "bing", "label": "Bing", "field": "bing"},
    {"name": "yandex", "label": "Yandex", "field": "yandex"},
    {"name": "duckduckgo", "label": "DuckDuckGo", "field": "duckduckgo"},
    {"name": "brave", "label": "Brave", "field": "brave"},
    {"name": "baidu", "label": "Baidu", "field": "baidu"},
]

column_defaults = {
    "align": "center",
    "headerClasses": "uppercase text-primary",
    "style": "width: 80px",
}


def table_emotes(table):
    table.add_slot(
        "body-cell-native",
        """
        <q-td key="native" :props="props">
            <q-icon
                :name="props.value === 'yes' ? 'check' : props.value === 'no' ? 'close' : props.value === 'partial' ? 'sentiment_satisfied' : 'help_outline'"
                :color="props.value === 'yes' ? 'green' : props.value === 'no' ? 'red' : props.value === 'partial' ? 'orange' : 'grey'"
                size="md"
             />
        </q-td>
    """,
    )
    table.add_slot(
        "body-cell-google",
        """
        <q-td key="google" :props="props">
            <q-icon
                :name="props.value === 'yes' ? 'sentiment_very_satisfied' : props.value === 'no' ? 'sentiment_very_dissatisfied' : props.value === 'partial' ? 'sentiment_satisfied' : 'help_outline'"
                :color="props.value === 'yes' ? 'green' : props.value === 'no' ? 'red' : props.value === 'partial' ? 'orange' : 'grey'"
                size="md"
             />
        </q-td>
    """,
    )
    table.add_slot(
        "body-cell-bing",
        """
        <q-td key="bing" :props="props">
            <q-icon
                :name="props.value === 'yes' ? 'sentiment_very_satisfied' : props.value === 'no' ? 'sentiment_very_dissatisfied' : props.value === 'partial' ? 'sentiment_satisfied' : 'help_outline'"
                :color="props.value === 'yes' ? 'green' : props.value === 'no' ? 'red' : props.value === 'partial' ? 'orange' : 'grey'"
                size="md"
             />
        </q-td>
    """,
    )
    table.add_slot(
        "body-cell-yandex",
        """
        <q-td key="yandex" :props="props">
            <q-icon
                :name="props.value === 'yes' ? 'sentiment_very_satisfied' : props.value === 'no' ? 'sentiment_very_dissatisfied' : props.value === 'partial' ? 'sentiment_satisfied' : 'help_outline'"
                :color="props.value === 'yes' ? 'green' : props.value === 'no' ? 'red' : props.value === 'partial' ? 'orange' : 'grey'"
                size="md"
             />
        </q-td>
    """,
    )
    table.add_slot(
        "body-cell-duckduckgo",
        """
        <q-td key="duckduckgo" :props="props">
            <q-icon
                :name="props.value === 'yes' ? 'sentiment_very_satisfied' : props.value === 'no' ? 'sentiment_very_dissatisfied' : props.value === 'partial' ? 'sentiment_satisfied' : 'help_outline'"
                :color="props.value === 'yes' ? 'green' : props.value === 'no' ? 'red' : props.value === 'partial' ? 'orange' : 'grey'"
                size="md"
             />
        </q-td>
    """,
    )
    table.add_slot(
        "body-cell-brave",
        """
        <q-td key="brave" :props="props">
            <q-icon
                :name="props.value === 'yes' ? 'sentiment_very_satisfied' : props.value === 'no' ? 'sentiment_very_dissatisfied' : props.value === 'partial' ? 'sentiment_satisfied' : 'help_outline'"
                :color="props.value === 'yes' ? 'green' : props.value === 'no' ? 'red' : props.value === 'partial' ? 'orange' : 'grey'"
                size="md"
             />
        </q-td>
    """,
    )
    table.add_slot(
        "body-cell-baidu",
        """
        <q-td key="baidu" :props="props">
            <q-icon
                :name="props.value === 'yes' ? 'sentiment_very_satisfied' : props.value === 'no' ? 'sentiment_very_dissatisfied' : props.value === 'partial' ? 'sentiment_satisfied' : 'help_outline'"
                :color="props.value === 'yes' ? 'green' : props.value === 'no' ? 'red' : props.value === 'partial' ? 'orange' : 'grey'"
                size="md"
             />
        </q-td>
    """,
    )


def operators_table() -> None:
    """Build and display the operators table."""
    with ui.column().style("width:600px"):
        with ui.row():
            elements.ToggleButton("Operators", color="#e6e6e6").on_click(
                lambda: app.storage.user.update(
                    view_operators=(
                        False if app.storage.user["view_operators"] is True else True
                    )
                )
            )
        with ui.row().bind_visibility_from(app.storage.user, "view_operators"):
            with ui.column().style("color: #555;"):
                ui.label("Compatible operators with Dorky.")
                ui.html(
                    "They are mainly Google search operators, but few of them are custom made like <code>lang:</code>, <code>country:</code>, <code>sub:</code> or <code>last:</code>.",
                )

            with ui.row().style("color: #555;"):
                for operator in operator_list:
                    with ui.card().classes("no-shadow border-[1px]").style(
                        "margin: 0px; padding: 0; width:600px"
                    ):
                        op_rows = [operator["table"]]
                        with ui.row().style(
                            "align-items: center; margin:0px; padding:5px 10px; background-color: #f5f5f5; width:100%;"
                        ):
                            ui.label(operator["table"]["operator"]).style(
                                "font-size: 16px; font-weight: bold; color: #3b82f6"
                            )
                            ui.html(operator["description"]).style(
                                "font-size: 14px; color: #15141A;"
                            )

                        with ui.column().style("margin:0px; padding:0 10px 10px 10px;"):
                            table = (
                                ui.table(
                                    columns=columns,
                                    column_defaults=column_defaults,
                                    rows=op_rows,
                                    row_key="name",
                                )
                                .props("flat bordered dense")
                                .style("margin-left: 40px;")
                            )
                            table_emotes(table)

                            for example in operator["examples"]:
                                with ui.row().style(
                                    "margin:0px; padding:0px; align-items:center;"
                                ):
                                    ui.label(example["example"]).style(
                                        "font-size:13px; padding:9px; border:1px solid #ededf0; border-radius:4px;"
                                    ).props()
                                    ui.html(example["explanation"]).style(
                                        "font-size: 14px; margin:0px; padding:0px;"
                                    )

                            if notes := operator.get("notes"):
                                for note in notes:
                                    with ui.row().style(
                                        "margin:0px; padding:0px; align-items:center;"
                                    ):
                                        message = ""
                                        if note.get("engine"):
                                            if (
                                                operator["table"][note["engine"]]
                                                == "no"
                                            ):
                                                color = "#f44336"
                                            elif (
                                                operator["table"][note["engine"]]
                                                == "partial"
                                            ):
                                                color = "#ff9900"
                                            message += f'<span style="color: {color};">{note['engine'].capitalize()}</span>: '
                                        message += note["note"]
                                        ui.html(message)
