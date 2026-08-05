from services.ai_service import AIService

ai = AIService("gemini")

result = ai.generate(
    "Say hello in one sentence."
)

print(result)