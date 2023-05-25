# -*- coding: utf-8 -*-
"""Let's build an executable for Comodoro"""

from cx_Freeze import setup, Executable
import sys

from appinfo import appInfo


base = "Win32GUI" if sys.platform == "win32" else None
executables = [
        Executable("main.pyw", base=base, target_name=appInfo.appName),
        Executable("runEngine.py", target_name='engine')
        ]
options = {
        "build_exe": {
            "packages": [],
            "includes": [],
            "excludes": ['tkinter', 'multiprocessing', 'ensurepip', 'test'],
            "include_files": ['config_spec.ini', 'sounds'],
            }
        }

setup(
        name=appInfo.appName,
        description=appInfo.description,
        version=appInfo.version,
        options=options,
        executables=executables
        )
