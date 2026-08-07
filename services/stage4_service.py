class Stage4Service:

    def generate(
        self,
        gospel: str,
        language: str,
        audience: str,
    ) -> str:

        return f"""# METADATA

AUTHOR=Luminous Journey

GOSPEL={gospel}

LANGUAGE={language}

AUDIENCE={audience}

VERSION=1.0

GENERATED_BY=Luminous Journey Studio
"""