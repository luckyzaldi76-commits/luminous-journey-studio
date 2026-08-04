from services.openrouter_service import generate


class AIGenerator:

    MAX_PROMPT_LENGTH = 30000

    def generate(self, prompt):

        print()
        print("=" * 60)
        print("AI GENERATION")
        print("=" * 60)

        print(f"Prompt Length : {len(prompt):,} characters")

        if len(prompt) > self.MAX_PROMPT_LENGTH:

            raise ValueError(
                f"Prompt terlalu panjang ({len(prompt):,} karakter).\n"
                f"Maksimum: {self.MAX_PROMPT_LENGTH:,}"
            )

        print("Sending request to OpenRouter...")

        response = generate(prompt)

        print("AI Generation Finished.")

        return response


_generator = AIGenerator()


def generate_content(prompt):

    return _generator.generate(prompt)