# -*- coding: utf-8 -*-
"""
Setup the logging for the app
"""

import os
import sys
import logging

from app_info import appName


def setup():
    """Create the logging file and setup the logging handler"""
    if getattr(sys, 'frozen', False):
        # Running as an executable
        if sys.platform == 'win32':
            log_dir = os.path.join(os.environ['APPDATA'], appName, "logs")
        elif sys.platform == 'linux':
            log_dir = os.path.join(os.path.expanduser('~'), ".local", "shared", appName.lower(), "logs")
        elif sys.platform == 'darwin':
            log_dir = os.path.join(os.path.expanduser('~'), "Library", "Application Support", appName, "logs")
    else:
        # Running from source
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, "app.log")
    
    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_file,
        filemode='w',
        encoding='utf-8',
        format='%(levelname)s - %(module)s: %(message)s'
    )
