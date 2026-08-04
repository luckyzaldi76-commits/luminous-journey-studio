from services.gemini_service import generate


def generate_content(prompt):
    print("\nMenghubungi AI...\n")

    result = generate(prompt)

    print("AI selesai.\n")

    return result