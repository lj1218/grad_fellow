# -*- coding:utf-8 -*-
"""Logger module."""
import logging
import logging.handlers


def setup_logger(app):
    """Set up logger."""
    logger = app.logger
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        '[%(asctime)s][%(levelname)s][%(filename)s]' +
        '[%(lineno)d] %(message)s', '%Y%m%d %H:%M:%S'
    )

    # setup cmd logger
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    cmd_level = app.config.get('LOGGER_CMD_LEVEL') or logging.INFO
    sh.setLevel(cmd_level)
    logger.addHandler(sh)

    # setup file logger
    rotating_file_conf = app.config.get('LOGGER_ROTATING_FILE_CONF')
    if rotating_file_conf is not None:
        # Add the log message handler to the logger
        log_filename = rotating_file_conf.get('logFilename') or 'app.log'
        max_bytes = rotating_file_conf.get('maxBytes') or 1024 * 1024  # 1MB
        backup_count = rotating_file_conf.get('backupCount') or 2
        rfh = logging.handlers.RotatingFileHandler(
            log_filename, maxBytes=max_bytes, backupCount=backup_count)
        rfh.setFormatter(fmt)
        file_level = app.config.get('LOGGER_FILE_LEVEL') or logging.DEBUG
        rfh.setLevel(file_level)
        logger.addHandler(rfh)
    return logger


def get_logger(name=None, cmd_level=logging.INFO, file_level=logging.DEBUG,
               rotating_file_conf=None):
    """Get logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        '[%(asctime)s][%(levelname)s][%(filename)s]' +
        '[%(lineno)d] %(message)s', '%Y%m%d %H:%M:%S'
    )

    # setup cmd logger
    sh = logging.StreamHandler()
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
    return logger
