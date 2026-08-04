from services.ai_service import AIService

ai = AIService("gemini")

response = ai.generate("Say Hello")

print(response)