import logging

import graypy


def get_logger(name, graylog_logger_address, level: int = logging.DEBUG):
    logger = logging.getLogger(name)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    host, port = graylog_logger_address.split(":")
    handler = graypy.GELFTCPHandler(host, int(port))
    logger.addHandler(handler)

    logger.setLevel(level)
    return logger
