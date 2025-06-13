import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    numeric_level = getattr(logging, "INFO", logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)
    
    # Prevent propagation to the root logger to avoid duplicate logs
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(numeric_level)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
