from docx import Document
from config import PROMPT_FILE


def load_prompt():

    doc = Document(PROMPT_FILE)

    text = []

    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text)

    return "\n".join(text)