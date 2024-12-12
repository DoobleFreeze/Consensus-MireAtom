import logging.config
import logging
import yaml
from flask import Flask


def get_logger(logging_cfg_path: str, flask_log: bool, flask_app: Flask = None) -> logging.Logger:
    """
    Инициализация логирования.

    Создает оператор логирования с учетом конфигурации, прописанной в файле.
    Путь к файлу передается как строковый параметр.

    Arguments:
        logging_cfg_path (str): Путь до файла с конфигурацией
        flask_log (bool): Включать ли логирование от Flask
        flask_app (Flask): Объект класса API

    Returns:
        logging.Logger: Оператор логирования.
    """
    if flask_log:
        flask_app.logger.disabled = True
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    logger_api = logging.getLogger('consensus_log')

    with open(logging_cfg_path) as config_fin:
        logging.config.dictConfig(yaml.safe_load(config_fin.read()))

    logger_api.handlers.pop()

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())

    logger_api.addHandler(ch)

    return logger_api


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s | %(levelname)s]: %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

