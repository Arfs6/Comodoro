# -*- coding: utf-8 -*-
"""Have functions that returns which path to use based on the current os the
code is running on
"""

import os
from platform import system
import sys
from typing import Union

from appinfo import appInfo


runningPlatform = system()
installed = False


def configPath(isspec=False):
    """Returns path to store config file.
    Creates folder if it doesn't exists.
    Parameter:
    - isspec: When true, returns path to config spec file
    """
    path: Union[None, str] = None
    if installed:
        if runningPlatform == "Windows":
            # Windows
            path = os.path.join(os.getenv('APPDATA'), appInfo.appname)
        elif runningPlatform == "Linux":
            # Linux
            path = os.path.expanduser(f"~/.config/{appInfo.appname}")
        elif runningPlatform == "Darwin":
            # macOS
            path = os.path.expanduser(
                    f"~/Library/Application Support/{appInfo.appname}")
    if not installed or not path:
        # Unsupported platform or running from source
        path = os.getcwd()

    if not os.path.exists(path):
        os.makedirs(path)

    return os.path.join(path, 'config.ini') if not isspec else os.path.join(path,
                                                                      'config_spec.ini')


def logsPath(gui=False):
    """Return the path where the log files are stored"""
    logDir: Union[None, str] = None
    if installed:
        if runningPlatform == "Windows":
            logDir = os.path.join(os.environ['APPDATA'], appInfo.appname, "logs")
        elif runningPlatform == "Linux":
            logDir = os.path.join(os.path.expanduser('~'), ".local", "shared",
                                  appInfo.appname, "logs")
        elif runningPlatform == "Darwin":
            logDir = os.path.join(os.path.expanduser('~'), "Library",
                                   "Application Support", appInfo.appname, "logs")
    if not installed or not logDir:
        # Running from source or unsupported platform
        logDir = os.path.join(os.getcwd(), "logs")

    if not os.path.exists(logDir):
        os.makedirs(logDir)
    
    logFileName: str = appInfo.appname if not gui else appInfo.appname + '-gui'
    logFile: str = os.path.join(logDir, f"{logFileName}.log")
    return logFile
