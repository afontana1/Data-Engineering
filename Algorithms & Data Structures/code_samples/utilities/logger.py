import logging
import sys
import os
from logging import Logger
from logging.handlers import RotatingFileHandler


class CustomLogger(Logger):
    def __init__(
        self,
        log_path="",
        log_file="",
        log_format="%(asctime)s, %(levelname)-8s [%(filename)-30s:%(lineno)d] : %(message)s",
        *args,
        **kwargs,
    ):
        self.formatter = logging.Formatter(log_format)
        self.log_file = log_file
        self.log_path = f'{os.path.abspath(".")}/{log_path}'

        Logger.__init__(self, *args, **kwargs)

        if (self.log_path) and (not os.path.isdir(self.log_path)):
            os.mkdir(self.log_path)

        self.addHandler(self.get_console_handler())
        if log_file:
            self.addHandler(self.get_file_handler())

        # with this pattern, it's rarely necessary to propagate the| error up to parent
        self.propagate = False

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        console_handler.setLevel(logging.INFO)
        return console_handler

    def get_file_handler(self):
        file_handler = logging.FileHandler(f"{self.log_path}/{self.log_file}")
        file_handler.setFormatter(self.formatter)
        file_handler.setLevel(logging.INFO)
        return file_handler


def custom_logger(logPath=None, fileName=None):
    """Custom Logger that outputs to console and file.

    Args:
        logPath (str): directory containing log file
        fileName (str): name of file
    Return:
        configured Logger
    """
    logPath = (
        os.path.abspath(".") + "/" + logPath
        if logPath
        else os.path.abspath(".") + "/logs"
    )
    fileName = (
        os.path.basename(fileName).split(".")[0]
        if fileName
        else os.path.basename(__file__).split(".")[0]
    )

    if not os.path.isdir(logPath):
        os.mkdir(logPath)

    print(logPath)
    print(fileName)
    logFormatter = logging.Formatter(
        "%(asctime)s, %(levelname)-8s [%(filename)-30s:%(lineno)d] : %(message)s"
    )
    logger = logging.getLogger()
    logger.setLevel(
        logging.DEBUG
    )  # this is needed to get all levels, and therefore filter on each handler

    # fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName)) # this is for regular file handler
    fileHandler = RotatingFileHandler(
        "{0}/{1}.log".format(logPath, fileName), maxBytes=(1048576 * 5), backupCount=3
    )
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    logger.addHandler(consoleHandler)

    return logger
