# -*- coding: utf-8 -*-
"""
Does all the necessary setup and start the main loop for the app
"""

import subprocess
import os
import sys

import gui


def run() -> None:
    """Starts the engine and then the gui `for now`"""
    subprocess.Popen([sys.executable, 'runEngine.py'])
    gui.run()


if __name__ == '__main__':
    run()
