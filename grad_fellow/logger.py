# -*- coding:utf-8 -*-
"""Logger module."""
import logging

from .common.logger import get_logger

logger = get_logger(name=__name__, cmd_level=logging.DEBUG,
                    rotating_file_conf={})
