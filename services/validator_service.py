class ValidatorService:

    @staticmethod
    def require_sections(
        response: str,
        *sections: str,
    ):

        missing = []

        for section in sections:

            if f"# {section}" not in response:

                missing.append(section)

        if missing:

            raise RuntimeError(
                "Missing markdown section(s): "
                + ", ".join(missing)
            )