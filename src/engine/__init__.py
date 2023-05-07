# -*- coding: utf-8 -*-
"""
This is the engine of comodoro. It is like a service that the view part of the
app communicates with. communication is done via socket (check messenger.py).
"""

import sys
from logging import getLogger

import logger
logger.setup()
from .controller import Controller


log = getLogger(__name__)


def run():
    sys.excepthook = logUnhandledExceptions
    Controller()


def logUnhandledExceptions(excType: type, excValue: Exception, traceback)\
        -> None:
    """Writes the unhandled exception as an Warning to the log file"""
    log.warning("Uncaught exception", exc_info=(excType, excValue, traceback),
                stack_info=True, stacklevel=2)
