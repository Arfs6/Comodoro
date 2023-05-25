# -*- coding: utf-8 -*-
"""
Does all the necessary setup and start the main loop for the app
"""

import subprocess
import os
import sys

import paths
if os.path.exists('uninstall.exe'):
    paths.installed = True
import gui


def run() -> None:
    """Starts the engine and then the gui `for now`"""
    if getattr(sys, 'frozen', False):
        engine = 'engine.exe' if sys.platform == 'win32' else 'engine'
        subprocess.Popen(engine)
    else:
        engine = 'runEngine.py'
        subprocess.Popen([sys.executable, engine])
    gui.run()


if __name__ == '__main__':
    run()
