# -*- coding:utf-8 -*-
"""Logger module."""
import logging
import logging.handlers

from flask import request
from flask.logging import default_handler, wsgi_errors_stream


class RequestFormatter(logging.Formatter):
    """Request formatter to inject Request Information."""

    def format(self, record):
        """Format the specified record as text."""
        record.remote_addr = request.remote_addr
        record.path = request.path
        record.method = request.method
        return super().format(record)


def init_logger(name_list=None, cmd_level=logging.INFO,
                file_level=logging.DEBUG, rotating_file_conf=None,
                propagate=True):
    """Init logger."""
    logger = None
    for name in name_list:
        logger = logging.getLogger(name)
        logger.propagate = propagate
        configure_logging(logger, cmd_level, file_level,
                          rotating_file_conf)
    return logger


def configure_flask_logging(app):
    """Configure flask logging."""
    logger = app.logger
    logger.removeHandler(default_handler)
    cmd_level = app.config.get('LOGGER_CMD_LEVEL') or logging.INFO
    file_level = app.config.get('LOGGER_FILE_LEVEL') or logging.DEBUG
    rotating_file_conf = app.config.get('LOGGER_ROTATING_FILE_CONF')
    configure_logging(logger, cmd_level, file_level, rotating_file_conf)


def configure_logging(logger, cmd_level, file_level, rotating_file_conf):
    """Configure logging."""
    logger.setLevel(logging.DEBUG)
    fmt = RequestFormatter(
        '[%(asctime)s][%(levelname)-5s][%(remote_addr)s][%(method)s %(path)s]'
        '[%(name)s][%(filename)s][%(lineno)d] %(message)s', '%Y%m%d %H:%M:%S'
    )

    # setup cmd logger
    sh = logging.StreamHandler(wsgi_errors_stream)
    sh.setFormatter(fmt)
    sh.setLevel(cmd_level)
    logger.addHandler(sh)

    # setup file logger
    if rotating_file_conf is not None:
        # Add the log message handler to the logger
        log_filename = rotating_file_conf.get('logFilename') or 'app.log'
        max_bytes = rotating_file_conf.get('maxBytes') or 1024 * 1024  # 1MB
        backup_count = rotating_file_conf.get('backupCount') or 2
        rfh = logging.handlers.RotatingFileHandler(
            log_filename, maxBytes=max_bytes, backupCount=backup_count)
        rfh.setFormatter(fmt)
        rfh.setLevel(file_level)
        logger.addHandler(rfh)
