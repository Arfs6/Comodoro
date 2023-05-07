# -*- coding: utf-8 -*-
"""Have functions that returns which path to use based on the current os the
code is running on
"""

import os
from platform import system
import sys

from appinfo import appInfo


runningPlatform = system()


def configPath(isspec=False):
    """Returns path to store config file.
    Creates folder if it doesn't exists.
    Parameter:
    - isspec: When true, returns path to config spec file
    """
    if not getattr(sys, 'frozen', False):
        # Not running as executable
        path = os.getcwd()
    elif runningPlatform == "Windows":
        # Windows
        path = os.path.join(os.getenv('APPDATA'), appInfo.appname, 'config.ini')
    elif runningPlatform == "Linux":
        # Linux
        path = os.path.expanduser(f"~/.config/{appInfo.appname}")
    elif runningPlatform == "Darwin":
        # macOS
        path = os.path.expanduser(
                f"~/Library/Application Support/{appInfo.appname}")
    else:
        # Unsupported platform
        path = os.getcwd()

    if not os.path.exists(path):
        os.makedirs(path)

    return os.path.join(path, 'config.ini') if not isspec else os.path.join(path,
                                                                      'config_spec.ini')


def logsPath(gui=False):
    """Return the path where the log files are stored"""
    if not getattr(sys, 'frozen', False):
        # Running from source
        logDir = os.path.join(os.getcwd(), "logs")
    elif runningPlatform == "Windows":
        logDir = os.path.join(os.environ['APPDATA'], appInfo.appname, "logs")
    elif runningPlatform == "Linux":
        logDir = os.path.join(os.path.expanduser('~'), ".local", "shared",
                              appInfo.appname, "logs")
    elif runningPlatform == "Darwin":
        logDir = os.path.join(os.path.expanduser('~'), "Library",
                               "Application Support", appInfo.appname, "logs")
        if not os.path.exists(logDir):
            os.makedirs(logDir)
    
    logFileName = appInfo.appname if not gui else appInfo.appname + '-gui'
    logFile = os.path.join(logDir, f"{logFileName}.log")
    return logFile
