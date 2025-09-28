import json
import re
import urllib.parse
from datetime import datetime

from dorky import json_data_dir


class Search:
    """Class to convert search queries"""
    def __init__(self, query, query_engines: list):
        self.query = query
        self.query_engines = query_engines
        self.engines = self.load_engines()
        self.wildcard_pattern = re.compile(r'"[^"]*\*[^"]*"')

    def get_engines_conf(self) -> list:
        """Load the search engines configuration based on the chosen engines."""
        with open(f"{json_data_dir}/search_engines.json", "r", encoding="utf-8") as f:
            engines_conf = json.load(f)
        return [
            engine for engine in engines_conf if engine["name"] in self.query_engines
        ]

    @staticmethod
    def get_yandex_countries() -> list:
        """Load Yandex country codes;"""
        with open(f"{json_data_dir}/yandex_countries.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def load_engines(self) -> list:
        """Get the search engines configuration."""
        engines_conf = self.get_engines_conf()
        engine_set = self.query_engines
        # Engine override for special operators
        if "sub:" in self.query:
            engine_set = ["Google", "Yandex"]
        if "last:" in self.query or "!IP" in self.query:
            engine_set = ["Google"]
        # Retrieve the configuration for the selected search engines
        engines = [engine for engine in engines_conf if engine["name"] in engine_set]
        return engines

    @staticmethod
    def delete_keyword(query, match_group) -> str:
        """Delete a keyword from the query"""
        return query.replace(match_group, "")

    @staticmethod
    def delete_keywords(query, keywords: list, space=False) -> str:
        """Delete keywords from the query"""
        for keyword in keywords:
            try:
                token = " " + keyword.group() if space else keyword.group()
                query = query.replace(token, "")
            except AttributeError:
                pass
        return query

    @staticmethod
    def get_operator_and_value(query, operator) -> re.Match or None:
        """Search for an operator and its following value"""
        return re.search(rf'{operator.lstrip(" ")}(\S+)', query)

    @staticmethod
    def get_operator_value(match_group) -> str:
        """Extract the value from an operator"""
        return match_group.split(":")[1].strip().rstrip('"')

    @staticmethod
    def convert_keyword(query, operator, keyword) -> str:
        """Replace an operator with its corresponding one"""
        return query.replace(operator, keyword)

    @staticmethod
    def days_since_epoch(date: datetime) -> int:
        """Return the number of days from the Unix epoch"""
        epoch_date = datetime(1970, 1, 1)
        difference = date - epoch_date
        return difference.days

    @staticmethod
    def validate_date(date_str) -> str or None:
        """Check if a date is formatted like YYYY-MM-DD"""
        error_message = "before: and after: format should be YYYY-MM-DD like 2025-01-01 or 2025-01-31."
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            if not (1 <= date.month <= 12 and 1 <= date.day <= 31):
                return error_message
        except ValueError:
            return error_message
        return None

    @staticmethod
    def format_date(date_str) -> str:
        """Format the date string into YYYY-MM-DD format if given without the 0"""
        date = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date.strftime("%Y-%m-%d")
        return formatted_date

    @staticmethod
    def check_in_quotation(query, operator) -> bool:
        """Check if the operator is within quotation marks"""
        return re.search(rf'"[^"]*{re.escape(operator)}[^"]*"', query) is not None

    @staticmethod
    def revert_domain(domain: str) -> str:
        """Revert domain name notation"""
        domain = domain.split(".")
        domain.reverse()
        return ".".join(domain)

    @staticmethod
    def check_last_value(value: str) -> bool:
        """Check if the last: operator value is valid (for last:)"""
        return bool(re.fullmatch(r"\d+[smhSMH]", value))

    def convert(self) -> dict:
        """Convert the operators in the query to the corresponding search engine URLs"""
        converted_queries = []

        for engine in self.engines:
            operators = engine["operators"]
            url = engine["url"]
            query = self.query

            # Handle dates
            if any(op in query for op in ["before:", "after:"]):
                date_handler = self.HandleDates(self, query, engine)
                if hasattr(date_handler, "error"):
                    return {"status": "error", "error": date_handler.error}
                query, chunk_result = date_handler.process_dates()
                if chunk_result:
                    url += chunk_result

            # Handle main operators
            for operator, details in operators.items():
                if operator != "*" and self.check_in_quotation(query, operator):
                    continue
                if operator in query:
                    # keword switch
                    if details["type"] == "keyword":
                        query = self.convert_keyword(
                            query, operator, details["keyword"]
                        )
                    # handle url type
                    elif details["type"] == "url":
                        if match := self.get_operator_and_value(query, operator):
                            operator_value = self.get_operator_value(match.group())
                            if engine["name"] == "Google" and operator == "country:":
                                operator_value = operator_value.upper()
                            chunk = details["chunk"].format(operator_value)
                            query = self.delete_keywords(query, [match])
                            url += chunk
                    # handle a split if * is not supported
                    elif details["type"] == "wildcard" and details["action"] == "split":
                        if matches := self.wildcard_pattern.findall(query):
                            for match in matches:
                                query = self.delete_keyword(query, match).strip()
                                splits = match.split("*")
                                converted_splits = [
                                    f'"{split.strip().replace('"', "").strip()}"'
                                    for split in splits
                                    if split != " "
                                ]
                                converted_splits = [
                                    split for split in converted_splits if split != '""'
                                ]
                                query += " " + " ".join(converted_splits)
                    # handle some Yandex special operators
                    elif details["type"] == "special" and engine["name"] == "Yandex":
                        operator_value = None
                        match = None
                        if operator == "country:":
                            yandex_countries = self.get_yandex_countries()
                            if match := self.get_operator_and_value(query, operator):
                                operator_value = self.get_operator_value(match.group())
                                operator_value = next(
                                    (
                                        country["yandex_code"]
                                        for country in yandex_countries
                                        if country["code"] == operator_value.upper()
                                    ),
                                    84,
                                )
                        elif operator == " lang:":
                            if match := self.get_operator_and_value(query, operator):
                                operator_value = self.get_operator_value(match.group())
                        chunk = details["chunk"].format(operator_value)
                        query = self.delete_keywords(query, [match])
                        url += chunk
                    # sub: handling
                    elif operator == "sub:" and details["type"] == "transform":
                        if match := self.get_operator_and_value(query, operator):
                            operator_value = self.get_operator_value(match.group())
                            if engine["name"] == "Google":
                                new_operator = f"site:*.{operator_value} -site:www.{operator_value}"
                                query = query.replace(match.group(), new_operator)
                            if engine["name"] == "Yandex":
                                rhost = self.revert_domain(operator_value)
                                new_operator = f"rhost:{rhost}.*"
                                query = query.replace(match.group(), new_operator)
                    # handle last: operator
                    elif operator == "last:" and details["type"] == "special":
                        if match := self.get_operator_and_value(query, operator):
                            operator_value = self.get_operator_value(match.group())
                            chunk = ""
                            if engine["name"] == "Google" and self.check_last_value(
                                operator_value
                            ):
                                if operator_value[-1].lower() == "s":
                                    lasting = operator_value[:-1]
                                    chunk = f"&tbs=qdr:s{lasting}"
                                if operator_value[-1].lower() == "m":
                                    lasting = operator_value[:-1]
                                    chunk = f"&tbs=qdr:n{lasting}"
                                if operator_value[-1].lower() == "h":
                                    lasting = operator_value[:-1]
                                    chunk = f"&tbs=qdr:h{lasting}"
                                query = self.delete_keywords(query, [match])
                                before_match = self.get_operator_and_value(
                                    query, "before:"
                                )
                                query = self.delete_keywords(query, [before_match])
                                after_match = self.get_operator_and_value(
                                    query, "after:"
                                )
                                query = self.delete_keywords(query, [after_match])
                                url += chunk
                    # handle !IP: operator
                    elif operator == "!IP" and details["type"] == "special":
                        ip_queries = self.ip_google(query)
                        for ip_query in ip_queries:
                            ip_query = ip_query.replace(" !IP", "").replace("!IP ", "").replace(" !IP ", "")
                            # ip_query = urllib.parse.quote(ip_query)
                            converted_queries.append(url.format(ip_query))
                    # delete unsupported operator
                    elif details["type"] == "delete":
                        if match := self.get_operator_and_value(query, operator):
                            space = True if engine["name"] == "Baidu" else False
                            query = self.delete_keywords(query, [match], space=space)
                    # handle Yandex for AND
                    elif engine["name"] == "Yandex" and details["type"] == "rewrite":
                        if operator == " AND ":
                            query = self.convert_and_to_yandex(query)

            # Handle DuckDuckGo countries, with multiple languages support per country
            if engine["name"] == "DuckDuckGo" and " country:" in query:
                if match := self.get_operator_and_value(query, "country:"):
                    operator_value = self.get_operator_value(match.group())
                    with open(
                        f"{json_data_dir}/duckduckgo_countries.json",
                        "r",
                        encoding="utf-8",
                    ) as f:
                        duckduckgo_countries = json.load(f)
                    regions = next(
                        (
                            country[operator_value]
                            for country in duckduckgo_countries
                            if operator_value in country
                        ),
                        ["wt-wt"],
                    )
                    query = self.delete_keywords(query, [match], space=True)
                    chunk = engine["operators"]["country:"]["chunk"]
                    for region in regions:
                        region_url = f"{url}{chunk.format(region)}"
                        converted_queries.append(region_url.format(query))
            else:
                # URL encode the query except for Baidu
                if engine["name"] != "Baidu":
                    query = urllib.parse.quote(query)
                converted_queries.append(url.format(query))
                # Remove the non IP search with Google
                if engine["name"] == "Google" and "!IP" in self.query:
                    converted_queries = converted_queries[:-1]

        converted_queries.reverse()
        return {"status": "ok", "urls": converted_queries}

    # Adapted from https://github.com/SeifElsallamy/gip by Seif Elsallamy
    @staticmethod
    def ip_google(search):
        o = 32 - len(search.split())
        template = "site:*.*.{}.*"
        ip_queries = []
        step = o
        start = 0
        while start < 256:
            end = min(start + step, 256)
            parts = [template.format(ii) for ii in range(start, end)]
            query = " |".join(parts)
            query = f"{search} ({query})"
            ip_queries.append(query)
            start = end
        return ip_queries

    @staticmethod
    def convert_and_to_yandex(query: str) -> str:
        """Converts AND to Yandex +."""
        # Define operators that should not be prefixed with '+'
        special_operators = {
            "site:",
            "intitle:",
            "inurl:",
            "intext:",
            "filetype:",
            "ext:",
            "sub:",
            "rhost:",
            "last:",
        }

        # Replace 'AND' with space to keep implicit AND behavior
        query = re.sub(r"\bAND\b", " ", query)

        # Tokenize input while keeping quoted phrases, operators, parentheses, and '|'
        pattern = (
            r"(\(|\)|"
            r"-?\b(?:" + "|".join(special_operators) + r")[^\s]+|"
            r'"[^"]+"|'
            r"-?\b\w+\b|"
            r"\|)"
        )
        tokens = re.findall(pattern, query)

        yandex_dork = []
        inside_parentheses = False
        open_paren_count = 0

        for token in tokens:
            if token == "(":
                # Opening parenthesis
                yandex_dork.append(token)
                inside_parentheses = True
                open_paren_count += 1
            elif token == ")":
                # Closing parenthesis
                yandex_dork.append(token)
                open_paren_count -= 1
                # If we've closed all parentheses, switch off inside_parentheses
                if open_paren_count <= 0:
                    inside_parentheses = False
            elif token == "|":
                # Pipe operator with single spacing
                yandex_dork.append(f" {token} ")
            elif token.startswith("-") or any(
                token.startswith(op) for op in special_operators
            ):
                # Operators or negations untouched
                yandex_dork.append(token)
            elif token.startswith('"'):
                # Quoted string untouched
                yandex_dork.append(token)
            else:
                # Normal word outside parentheses gets '+'
                if inside_parentheses:
                    # Inside parentheses, keep it without '+'
                    yandex_dork.append(token)
                else:
                    yandex_dork.append(f"+{token}")

        # Close  open parentheses
        while open_paren_count > 0:
            yandex_dork.append(")")
            open_paren_count -= 1

        # Clean up spacing
        result = " ".join(yandex_dork)
        # Remove double spaces from inserting ' | ',...
        result = re.sub(r"\s{2,}", " ", result).strip()

        return result

    class HandleDates:
        """Subclass to handle dates per search engine"""

        def __init__(self, search_instance, query, engine):
            self.search_instance = search_instance
            self.query = query
            self.engine = engine
            self.before = None
            self.after = None
            self.before_parenthesis = False
            self.after_parenthesis = False
            self.before_dt = None
            self.after_dt = None
            self.before_dt_s = None
            self.after_dt_s = None
            self.chunk = engine.get("date_chunk")
            self.today = datetime.now().strftime("%Y-%m-%d")

            self.before_kv = self.search_instance.get_operator_and_value(
                query, "before:"
            )
            self.after_kv = self.search_instance.get_operator_and_value(query, "after:")

            if self.before_kv:
                self.before = self.search_instance.get_operator_value(
                    self.before_kv.group()
                )
                validation = self.search_instance.validate_date(self.before)
                if validation:
                    self.error = validation
                    return
                self.before = self.search_instance.format_date(self.before)
                self.before_dt = datetime.strptime(self.before, "%Y-%m-%d")
                self.before_dt_s = self.before_dt.strftime("%Y%m%d")

            if self.after_kv:
                self.after = self.search_instance.get_operator_value(
                    self.after_kv.group()
                )
                validation = self.search_instance.validate_date(self.after)
                if validation:
                    self.error = validation
                    return
                self.after = self.search_instance.format_date(self.after)
                self.after_dt = datetime.strptime(self.after, "%Y-%m-%d")
                self.after_dt_s = self.after_dt.strftime("%Y%m%d")

        def process_dates(self) -> tuple:
            """Map date methods per engine name"""
            engine_handlers = {
                "Google": lambda: self.handle_google(),
                "Bing": lambda: self.handle_bing(),
                "Yandex": lambda: self.handle_yandex(),
                "Brave": lambda: self.handle_brave(),
                "DuckDuckGo": lambda: self.handle_duckduckgo(),
                "Baidu": lambda: self.handle_baidu(),
            }
            # Execute the appropriate handler method
            if self.engine["name"] in engine_handlers:
                return engine_handlers[self.engine["name"]]()
            return self.query, None

        def handle_google(self) -> tuple:
            """Handle Google date"""
            if self.before_kv:
                self.query = self.query.replace(
                    self.before_kv.group(), f"before:{self.before}"
                )
            if self.after_kv:
                self.query = self.query.replace(
                    self.after_kv.group(), f"after:{self.after}"
                )
            return self.query, None

        def handle_bing(self) -> tuple:
            """Handle Bing date"""
            before_days = (
                self.search_instance.days_since_epoch(self.before_dt)
                if self.before
                else self.search_instance.days_since_epoch(datetime.now())
            )
            after_days = (
                self.search_instance.days_since_epoch(self.after_dt)
                if self.after
                else 0
            )
            self.query = self.search_instance.delete_keywords(
                self.query, [self.before_kv, self.after_kv]
            )
            return self.query, self.chunk.format(after_days, before_days)

        def handle_yandex(self) -> tuple:
            """Handle Yandex date"""
            if self.before and self.after:
                if self.before == self.after:
                    self.query = self.query.replace(
                        self.before_kv.group(), f"date:{self.before_dt_s}"
                    )
                else:
                    self.query = self.query.replace(
                        self.before_kv.group(),
                        f"date:{self.after_dt_s}..{self.before_dt_s}",
                    )
            elif self.before and not self.after:
                self.query = self.query.replace(
                    self.before_kv.group(), f"date:<={self.before_dt_s}"
                )
            elif self.after and not self.before:
                self.query = self.query.replace(
                    self.after_kv.group(), f"date:>={self.after_dt_s}"
                )
            self.query = self.search_instance.delete_keywords(
                self.query, [self.before_kv, self.after_kv]
            )
            return self.query, None

        def handle_brave(self) -> tuple:
            """Handle Brave date"""
            if self.before and not self.after:
                self.after = datetime(1970, 1, 1).strftime("%Y-%m-%d")
            elif self.after and not self.before:
                self.before = self.today
            self.query = self.search_instance.delete_keywords(
                self.query, [self.before_kv, self.after_kv]
            )
            return self.query, self.chunk.format(self.after, self.before)

        def handle_duckduckgo(self) -> tuple:
            """Handle DuckDuckGo date"""
            if self.before and not self.after:
                self.after = datetime(1970, 1, 2).strftime("%Y-%m-%d")
            elif self.after and not self.before:
                self.before = self.today
            self.query = self.search_instance.delete_keywords(
                self.query, [self.before_kv, self.after_kv]
            )
            return self.query, self.chunk.format(self.after, self.before)

        def handle_baidu(self) -> tuple:
            """Handle Baidu date"""
            before_ts = (
                int(self.before_dt.timestamp())
                if self.before
                else int(datetime.now().timestamp())
            )
            after_ts = int(self.after_dt.timestamp()) if self.after else 0
            self.query = self.search_instance.delete_keywords(
                self.query, [self.before_kv, self.after_kv]
            )
            return self.query, self.chunk.format(after_ts, before_ts)
