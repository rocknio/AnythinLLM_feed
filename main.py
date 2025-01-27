import logging
import logging.handlers
import os
import sys

import book_utils
from book_utils.epub_utils import feed_all_books
from settings import load_settings


def init_logging():
    """
    日志文件设置
    """
    logger = logging.getLogger()
    logger.setLevel(20)
    if os.path.exists("log") is False:
        os.mkdir("log")

    sh = logging.StreamHandler()
    file_log = logging.handlers.TimedRotatingFileHandler('log/feed.log', 'D', 1, 0)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)-5s] [%(module)s:%(filename)s-%(funcName)s-%(lineno)d] %(message)s')
    sh.setFormatter(formatter)
    file_log.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(file_log)

    logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))


if __name__ == '__main__':
    init_logging()
    settings = load_settings()
    feed_all_books(settings)
    logging.info("Done")
