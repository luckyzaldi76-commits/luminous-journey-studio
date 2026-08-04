import time

from services.ai_generator import generate_content


class AIService:

    def generate(self, prompt):

        print()
        print("=" * 60)
        print("AI SERVICE")
        print("=" * 60)

        start = time.time()

        response = generate_content(prompt)

        if not response:

            raise RuntimeError(
                "AI Generation Failed."
            )

        elapsed = time.time() - start

        print()
        print(f"Response Length : {len(response):,} characters")
        print(f"Elapsed Time : {elapsed:.2f} sec")

        return response


ai_service = AIService()