# -*- coding: utf-8 -*-
"""
This is the engine of comodoro. It is like a service that the view part of the
app communicates with. communication is done via socket (check messenger.py).
"""

import sys
import os
from logging import getLogger

import logger
logger.setup()
from .controller import Controller


log = getLogger(__name__)


def run() -> None:
    """Perform pre-startup tasks and start controller"""
    log.debug("starting engine...")
    sys.excepthook = logUnhandledExceptions
    setVlcLib()
    Controller()


def logUnhandledExceptions(excType: type, excValue: Exception, traceback)\
        -> None:
    """Writes the unhandled exception as an Warning to the log file"""
    log.warning("Uncaught exception", exc_info=(excType, excValue, traceback),
                stack_info=True, stacklevel=2)


def setVlcLib() -> None:
    """Checks if app is frozen and set libvlc library"""
    if not getattr(sys, 'frozen', False):
        # running from source
        return

    if sys.platform == 'win32' and os.path.exists('libvlc.dll'):
        os.environ['PYTHON_VLC_LIB_PATH'] = os.path.join(os.getcwd(),
                                                         'libvlc.dll')
    # todo: do for other platforms
