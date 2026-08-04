from services.gemini_service import generate
from infrastructure.log.logger import get_logger

logger = get_logger(__name__)


def generate_content(prompt: str) -> str:
    logger.info("Menghubungi AI...")

    try:
        result = generate(prompt)

        logger.info("AI selesai.")

        return result

    except Exception:
        logger.exception("Terjadi kesalahan saat generate AI.")
        raise