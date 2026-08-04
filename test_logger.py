from infrastructure.log.logger import get_logger

logger = get_logger(__name__)

logger.info("Logger OK")
logger.warning("Warning OK")
logger.error("Error OK")