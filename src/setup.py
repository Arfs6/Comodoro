# -*- coding: utf-8 -*-
"""Let's build an executable for Comodoro"""

import sys
import os
import vlc
from cx_Freeze import setup, Executable
from typing import Union, List

from appinfo import appInfo


def run() -> None:
    """Start setup process"""
    base = "Win32GUI" if sys.platform == "win32" else None
    executables = [
            Executable("main.pyw", base=base, target_name=appInfo.appName),
            Executable("runEngine.py", base=base, target_name='engine')
            ]
    options = {
            "build_exe": {
                "packages": [],
                "includes": [],
                "excludes": ['tkinter', 'multiprocessing', 'ensurepip', 'test'],
                "include_files": ['config_spec.ini', 'sounds'] +
                getVlcLib(),
                }
            }

    setup(
            name=appInfo.appName,
            description=appInfo.description,
            version=appInfo.version,
            options=options,
            executables=executables
            )


def getVlcLib() -> List[str]:
    """Get location of vlc library"""
    path: Union[str, None] = vlc.find_lib()[1]
    if not path:
        return []

    paths: List[str] = [os.path.join(path, 'libvlc.dll')]
    paths.append(os.path.join(path, 'libvlccore.dll'))  # include libvlccore
    # include plugin folder
    # remove gui related plugins
    path = os.path.join(path, 'plugins')
    ls: List[str] = os.listdir(path)
    excludes: List[str] = ['control', 'gui', 'lua', 'plugins.dat', 'visualization']
    for file in ls:
        if file in excludes:
            continue
        source = os.path.join(path, file)
        dest = os.path.join('plugins', file)
        paths.append((source, dest))

    return paths


if __name__ == '__main__':
    run()
