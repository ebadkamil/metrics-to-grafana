"""
Metrics to grafana
Author: Ebad Kamil <ebad.kamil@ess.eu>
All rights reserved.
"""

import logging
from functools import wraps
from threading import Thread


def run_in_thread(original):
    @wraps(original)
    def wrapper(*args, **kwargs):
        t = Thread(target=original, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t

    return wrapper


def get_logger(name, level: int = logging.DEBUG):
    logger = logging.getLogger(name)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.setLevel(level)
    return logger
