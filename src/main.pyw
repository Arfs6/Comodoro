# -*- coding: utf-8 -*-
"""
Does all the necessary setup and start the main loop for the app
"""

from threading import Thread
import os
import sys

import paths
if os.path.exists('uninstall.exe'):
    paths.installed = True
import gui
import engine


def run() -> None:
    """Starts the engine and then the gui `for now`"""
    engine_thread = Thread(target=engine.run)
    engine_thread.start()
    gui.run()


if __name__ == '__main__':
    run()
