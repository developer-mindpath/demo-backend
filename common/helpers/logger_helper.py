import logging

logging.basicConfig(
    level=logging.INFO,
    format='\nLEVEL: %(levelname)s\t| TIMESTAMP: %(asctime)s\t| MESSAGE: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger()
