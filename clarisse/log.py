"""
Clarisse

log module.
Process global logging behavior.

by 1MLightyears@gmail.com

on 20201214
"""

import logging
import logging.config
import sys
import json
import os

info = logging.info
warning = logging.warning
error = logging.error
critical = logging.critical
fatal = logging.fatal
debug = logging.debug

### log settings
config = {
    "version": 1,
    "formatters": {
        "simple": {"format": "%(levelname)s : %(message)s"},
        "more": {"format": "%(asctime)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "more",
            "filename": "..\\Clarisse.log",
        },
    },
    "loggers": {"root": {"level": "WARNING", "handlers": ["console", "file"]}},
}
if os.path.exists("log_config.json"):
    with open("log_config.json", "r", encoding="utf-8") as f:
        config.update(json.load(f))
logging.config.dictConfig(config)
