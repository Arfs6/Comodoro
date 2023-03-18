# -*- coding: utf-8 -*-
"""
Does all the necessary setup and start the main loop for the app
"""

from logging import getLogger
import sys
import traceback
import wx

import logger
from gui import Application
from app_info import githubURL


def run():
    """Does setup and startthe main loop"""
    # Log any un-handled exception
    sys.excepthook = handle_unhandled_exception
    app = Application(redirect=True, filename='logs/stdio.log')
    log.debug('Starting main loop...')
    app.MainLoop()


def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    """
    Handle unhandled exceptions in the application.
    """
    log.error("Unhandled exception:", exc_info=(exc_type, exc_value, exc_traceback))

    try:
        # Display an error message to the user
        error_message = f"""An error occured while running the app.
Please go to {githubURL} and create an issue to inform the\
 developers"""
        wx.MessageBox(error_message, "Error", wx.OK | wx.ICON_ERROR)
    except wx.PyNoAppError:
        # create an App and inform the user?
        log.debug(f"An exception was raised and "
                f"no wx.App was found to inform the user")


if __name__ == '__main__':
    logger.setup()
    log = getLogger(__name__)
    log.debug('App starting...')
    run()
