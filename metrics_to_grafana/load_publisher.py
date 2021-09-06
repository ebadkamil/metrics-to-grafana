"""
Metrics to grafana
Author: Ebad Kamil <ebad.kamil@ess.eu>
All rights reserved.
"""
import argparse
import logging
import time
from getpass import getuser

import graphyte  # type: ignore
import psutil as ps

from metrics_to_grafana.utils import get_logger, run_in_thread


class LoadPublisher:
    def __init__(
        self,
        graphyte_server: str,
        logger: logging.Logger,
        prefix: str = "machine_info",
        update_interval_s: int = 10,
    ):
        self._graphyte_server = graphyte_server
        self._logger = logger
        self._update_interval_s = update_interval_s
        self._stop = False
        self._sender = graphyte.Sender(self._graphyte_server, prefix=prefix)

    @run_in_thread
    def start(self):
        while not self._stop:
            timestamp = time.time()
            memory = (ps.virtual_memory()).used / 1024 ** 3
            load = ps.cpu_percent()
            try:
                self._sender.send("cpu_load", load, timestamp)
                self._sender.send("memory", memory, timestamp)
                self._logger.debug(f"load {load}: memory {memory}")
            except Exception as ex:
                self._logger.error(f"Could not send load information: {ex}")
            time.sleep(self._update_interval_s)

    def stop(self):
        self._stop = True


def start_load_publisher():
    parser = argparse.ArgumentParser(prog="kafka application")
    parser.add_argument(
        "--grafana-carbon-address",
        required=True,
        help="<host[:port]> Address to the Grafana (Carbon) metrics server",
        type=str,
    )

    _log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    parser.add_argument(
        "--log-level",
        required=False,
        help="",
        choices=[level.upper() for level in _log_levels.keys()],
        type=lambda s: s.upper(),
        default="INFO",
    )

    args = parser.parse_args()

    logger = get_logger("Metrics Publisher", level=_log_levels[args.log_level])

    load_publisher = LoadPublisher(args.grafana_carbon_address, logger)
    try:
        load_publisher_t = load_publisher.start()
    except KeyboardInterrupt:
        logger.info(f"Interrupted by user: {getuser()}. Closing Publisher ...")
    finally:
        load_publisher.stop()
        load_publisher_t.join()
