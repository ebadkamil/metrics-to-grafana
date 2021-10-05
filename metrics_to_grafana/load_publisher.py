import logging
import time
from getpass import getuser
from socket import gethostname

import configargparse
import graphyte
import psutil as ps

from metrics_to_grafana.utils import get_logger

# See https://github.com/ess-dmsc/forwarder/blob/main/forwarder/statistics_reporter.py


class LoadPublisher:
    def __init__(
        self,
        server: str,
        logger: logging.Logger,
        prefix: str = "machine_info",
        update_interval: int = 1.0,
    ):
        self._server = server
        self._logger = logger
        self._update_interval = update_interval
        self._stop = False
        self._sender = graphyte.Sender(self._server, prefix=prefix)

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
            time.sleep(self._update_interval)

    def stop(self):
        self._stop = True


def start_load_publisher():
    parser = configargparse.ArgumentParser(prog="Metrics to grafana application")
    parser.add_argument(
        "-g",
        "--grafana-carbon-address",
        required=True,
        help="<host> Address to the Grafana (Carbon) metrics server. For eg. localhost",
        type=str,
        env_var="GRAFANA_ADDRESS",
    )

    parser.add_argument(
        "-gl",
        "--graylog-logger-address",
        required=True,
        help="<host[:port]> Address to the Graylog server. For eg. localhost:12201",
        env_var="GRAYLOG_ADDRESS",
    )

    _log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    parser.add_argument(
        "-l",
        "--log-level",
        required=False,
        help="",
        choices=[level.upper() for level in _log_levels.keys()],
        type=lambda s: s.upper().strip(),
        default="INFO",
        env_var="LOG_LEVEL",
    )
    parser.add_argument(
        "-c",
        "--config-file",
        required=False,
        is_config_file=True,
        help="Read configuration from an ini file",
        env_var="CONFIG_FILE",
    )

    args = parser.parse_args()
    print(args.config_file)
    logger = get_logger(
        "Metrics Publisher",
        graylog_logger_address=args.graylog_logger_address,
        level=_log_levels[args.log_level],
    )

    load_publisher = LoadPublisher(
        args.grafana_carbon_address, logger, prefix=f"{gethostname()}.machine_info"
    )
    try:
        load_publisher.start()
    except KeyboardInterrupt:
        logger.info(f"Interrupted by user: {getuser()}. Closing Publisher ...")
    finally:
        load_publisher.stop()
