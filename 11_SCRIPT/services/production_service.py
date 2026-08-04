from datetime import datetime

from core.find_reading import find_reading
from core.response_writer import save_response

from services.prompt_builder import build_prompt
from services.ai_service import ai_service
from services.parser_service import parser_service
from services.validation_service import validation_service
from services.builder_service import builder_service
from services.output_service import output_service


class ProductionService:

    def run(self):

        print()
        print("=" * 60)
        print("LUMINOUS JOURNEY PRODUCTION")
        print("=" * 60)

        while True:

            production_date = input(
                "Production Date (YYYY-MM-DD): "
            ).strip()

            try:

                datetime.strptime(
                    production_date,
                    "%Y-%m-%d"
                )

                break

            except ValueError:

                print("Invalid date.")

        print()
        print("STEP 1/6 Reading Lookup")

        reading = find_reading(
            production_date
        )

        if reading is None:

            print("Reading not found.")

            return

        print("OK")

        print()
        print("STEP 2/6 Build Prompt")

        prompt = build_prompt(
            reading
        )

        print("OK")

        print()
        print("STEP 3/6 AI Generation")

        response = ai_service.generate(
            prompt
        )

        output_dir = output_service.create(
            production_date
        )

        print()
        print("STEP 4/6 Save Response")

        save_response(
            response,
            output_dir / "response.md"
        )

        print("OK")

        print()
        print("STEP 5/6 Parse Markdown")

        data = parser_service.parse(
            response
        )

        print("OK")

        print()
        print("STEP 6/6 Validate")

        validation_service.validate(
            data
        )

        builder_service.build_all(
    data,
    output_dir
        )

        print()
        print("=" * 60)
        print("PRODUCTION SUCCESS")
        print("=" * 60)