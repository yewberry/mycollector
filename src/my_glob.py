# -*- coding: utf-8 -*-
import logging.handlers
import sys

formatter = logging.Formatter("%(asctime)s %(threadName)s(%(process)d/%(thread)d) %(levelname)-6s %(funcName)s/%(filename)s:%(lineno)d %(message)s")
file_handler = logging.handlers.RotatingFileHandler("my.log", maxBytes=1024*1024, backupCount=5)
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
_logger = logging.getLogger("mylogger")
_logger.addHandler(file_handler)
_logger.addHandler(stream_handler)
_logger.setLevel(logging.DEBUG)

LOG = _logger

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]