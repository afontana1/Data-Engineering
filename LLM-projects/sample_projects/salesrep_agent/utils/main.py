import atexit
import json
import logging.config
import logging.handlers
import pathlib
import queue

log_queue = queue.Queue(-1)
logger = logging.getLogger(__name__)
path_to_file = pathlib.Path(__file__).resolve().parent


def setup_logging():
    config_file = path_to_file / pathlib.Path("stderr-json-file.json")
    with open(config_file) as f_in:
        config = json.load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.handlers.QueueHandler(log_queue)
    if queue_handler is not None:
        queue_listener = logging.handlers.QueueListener(log_queue)
        queue_listener.start()
        atexit.register(queue_listener.stop)


def main():
    setup_logging()
    logging.basicConfig(level="INFO")
    logger.debug("debug message", extra={"x": "hello"})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()
