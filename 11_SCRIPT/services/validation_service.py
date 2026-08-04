class ValidationService:

    REQUIRED = [

        "TITLE",

        "SCRIPTURE",

        "THEME",

        "HISTORICAL BACKGROUND",

        "SCRIPTURE MEDITATION",

        "LIFE APPLICATION",

        "PRAYER",

        "KEY TAKEAWAYS",

    ]

    def validate(self, data):

        print()
        print("=" * 60)
        print("VALIDATION")
        print("=" * 60)

        missing = []

        for section in self.REQUIRED:

            if section in data:

                print(f"✔ {section}")

            else:

                print(f"✖ {section}")

                missing.append(section)

        if missing:

            raise RuntimeError(

                "Missing sections:\n\n"

                + "\n".join(missing)

            )

        print()
        print("Validation Passed.")


validation_service = ValidationService()