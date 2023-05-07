# -*- coding: utf-8 -*-
"""
Global app info like app anme are stored in this module
"""

class AppInfo:
    """Encapsulating all the info in a class to use the dot `.` notation when
    accessing the info.
    """
    appName = 'Comodaro'
    appname = appName.lower()
    githubURL = 'https://github.com/arfs6/comodoro'
    version = '0.1'


appInfo = AppInfo()
