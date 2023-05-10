# -*- coding: utf-8 -*-
"""
A GUI for the comodoro engine.
"""

import sys
import wx
from logging import getLogger

import logger
logger.setup(gui=True)
from appinfo import appInfo
from .mainview import Application
from .controller import Controller


log = getLogger(__name__)


def run() -> None:
    """Runs the GUI"""
    sys.excepthook = logUnhandledExceptions
    app = Application(redirect=True, filename='logs/gui-stdio.txt')
    controller = Controller()
    app.MainLoop()


def logUnhandledExceptions(excType: type, excValue: Exception, traceback)\
        -> None:
    """Writes the unhandled exception as an Warning to the log file"""
    log.warning("Uncaught exception", exc_info=(excType, excValue, traceback),
                stack_info=True, stacklevel=2)

    try:
        # Display an error message to the user
        error_message = f"""An error occured while running comodoro.
Please go to {appInfo.githubURL} and create an issue to inform the\
 developers"""
        wx.MessageBox(error_message, "Error", wx.OK | wx.ICON_ERROR)
    except wx.PyNoAppError:
        # The exception was before the wx.App object was initialized
        # create an App and inform the user?
        log.debug(f"An exception was raised and "
                f"no wx.App was found to inform the user")
