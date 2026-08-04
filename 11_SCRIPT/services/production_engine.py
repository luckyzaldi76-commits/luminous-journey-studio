from core.find_reading import find_reading
from core.response_writer import save_response

from services.prompt_builder import build_prompt
from services.ai_service import ai_service
from services.parser_service import parser_service
from services.validation_service import validation_service
from services.output_service import output_service
from services.builder_service import builder_service


class ProductionEngine:

    def process(
        self,
        production_date
    ):

        print()
        print("=" * 60)
        print(f"Production : {production_date}")
        print("=" * 60)

        # ---------------------------------------
        # Reading
        # ---------------------------------------

        reading = find_reading(
            production_date
        )

        if reading is None:

            print("Reading not found.")

            return False

        # ---------------------------------------
        # Prompt
        # ---------------------------------------

        prompt = build_prompt(
            reading
        )

        # ---------------------------------------
        # AI
        # ---------------------------------------

        response = ai_service.generate(
            prompt
        )

        # ---------------------------------------
        # Output Folder
        # ---------------------------------------

        output_dir = output_service.create(
            production_date
        )

        # ---------------------------------------
        # Save Response
        # ---------------------------------------

        save_response(
            response,
            output_dir / "response.md"
        )

        # ---------------------------------------
        # Parse
        # ---------------------------------------

        data = parser_service.parse(
            response
        )

        # ---------------------------------------
        # Validation
        # ---------------------------------------

        validation_service.validate(
            data
        )

        # ---------------------------------------
        # Builders
        # ---------------------------------------

        builder_service.build_all(
            data,
            output_dir
        )

        print()

        print("=" * 60)
        print("PRODUCTION SUCCESS")
        print("=" * 60)

        return True


production_engine = ProductionEngine()