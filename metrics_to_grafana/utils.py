"""
Metrics to grafana
Author: Ebad Kamil <ebad.kamil@ess.eu>
All rights reserved.
"""

import logging


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
