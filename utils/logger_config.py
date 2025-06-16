import logging
from logging import Logger

def setup_logger() -> Logger:
    """
        Configures and returns a logger with two handlers:
        - FileHandler to write logs to 'app.log' file with UTF-8 encoding
        - StreamHandler to output logs to the console

        Log format:
            '%(asctime)s - %(levelname)s - %(message)s'

        Logging level is set to INFO for both the logger and handlers.

        Handlers are added only if the logger has no handlers yet to avoid duplicates.

        Returns:
            Logger: the configured logger instance
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('app.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()