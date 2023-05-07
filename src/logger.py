# -*- coding: utf-8 -*-
"""
Setup the logging for the app
"""

import logging

import paths


def setup(gui=False):
    """Create the logging file and setup the logging handler"""
    logFile = paths.logsPath(gui)
    logging.basicConfig(
        level=logging.DEBUG,
        filename=logFile,
        filemode='w',
        encoding='utf-8',
        format='[%(asctime)s] - %(levelname)s - %(module)s: %(message)s',
        datefmt='%H:%M:%S'
    )
