import logging
import os
from re import L

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log_info(msg):
    logging.info(msg)

def log_error(msg):
    logging.error(msg)
