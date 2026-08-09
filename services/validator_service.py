from luminous.infrastructure.parsers.parser_service import ParserService


class ValidatorService:

    @classmethod
    def require_sections(
        cls,
        response: str,
        *sections: str,
    ) -> dict:

        cls.require_non_empty(
            response,
            "response",
        )

        parsed = ParserService.parse(
            response,
        )

        missing = []

        for section in sections:

            key = section.upper()

            value = parsed.get(
                key,
            )

            if value is None:

                missing.append(
                    section,
                )

                continue

            if not value.strip():

                missing.append(
                    section,
                )

        if missing:

            raise RuntimeError(
                "Missing or empty section(s): "
                + ", ".join(missing)
            )

        return parsed

    @staticmethod
    def require_non_empty(
        value: str,
        name: str,
    ) -> str:

        if not isinstance(
            value,
            str,
        ):

            raise TypeError(
                f"{name} must be a string."
            )

        if not value.strip():

            raise RuntimeError(
                f"{name} cannot be empty."
            )

        return value

    @staticmethod
    def require_dict(
        value,
        name: str,
    ):

        if not isinstance(
            value,
            dict,
        ):

            raise TypeError(
                f"{name} must be a dict."
            )

        return value