# -*- coding: utf-8 -*-
"""
Defines Gui classes for the app
"""

import wx
from logging import getLogger
from pubsub import pub

from appinfo import appInfo


log = getLogger(__name__)


def returnTrue():
    """A dummy function that returns True
    Used when overwriting `wx.TextControl.AcceptsFocusFromKeyboard` method.
    """
    return True


class Application(wx.App):
    def OnExit(self):
        """Perform clean up tasks"""
        log.debug("Exiting from application")
        pub.sendMessage('exit')
        return True

    def OnExceptionInMainLoop(self):
        """
        Handle unhandled exceptions during the main event loop.
        """
        log.debug('An exception was raised')
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # Log the exception
        log.error("Unhandled exception: ", exc_info=(exc_type, exc_value, exc_traceback))
        # Show an error message to the user
        wx.MessageBox(str(exc_value), "Error", wx.OK | wx.ICON_ERROR)
        # Continue processing events
        return True


class AppFrame(wx.Frame):
    """
    The main frame for the app. All other ui element are children of this
    element
    """

    def __init__(self):
        """Initialize app frame
        Parameter:
        -title: Title of the app
        """
        super().__init__(None, title=appInfo.appName, style=wx.DEFAULT_FRAME_STYLE |
                         wx.STATIC_BORDER)
        self.InitUI()

    def InitUI(self):
        """Initialize the Main UI"""
        log.debug('Initializing the Main frame UI')
        panel = wx.Panel(self)

        self.timerText = wx.TextCtrl(panel, value='00:00:00',
                                      style= wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB |
                                     wx.TE_READONLY | wx.BORDER_SIMPLE)
        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.timerText.SetFont(font)

        # progress bar
        self.timerProgress = wx.Gauge(panel, range=100, style=wx.GA_HORIZONTAL)

        # buttons
        self.settingsBtn = wx.Button(panel, label="Settings")
        self.mainBtn = wx.Button(panel, label="Start")
        self.helpBtn = wx.Button(panel, label="Help")

        # add icons to the buttons
        settings_icon = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
        self.settingsBtn.SetBitmap(settings_icon)
        
        help_icon = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_OTHER, (16, 16))
        self.helpBtn.SetBitmap(help_icon)

        # manage sizers
        topSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(self.timerText,
                     wx.SizerFlags(1).Expand().Border(wx.ALL, 10))
        topSizer.Add(self.timerProgress,
                     wx.SizerFlags(1).Expand().Border(wx.ALL, 10))

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)  # button row sizer
        btnSizer.Add(self.settingsBtn, wx.SizerFlags(0).Center())
        btnSizer.Add(self.mainBtn, wx.SizerFlags(0).Border(wx.ALL, 10).Center())
        btnSizer.Add(self.helpBtn, wx.SizerFlags(0).Center())
        topSizer.Add(btnSizer, 0, wx.EXPAND)
        panel.SetSizer(topSizer)

        # Enable tab traversal
        self.SetWindowStyle(wx.TAB_TRAVERSAL)
        self.timerText.AcceptsFocusFromKeyboard = returnTrue
        self.timerProgress.AcceptsFocusFromKeyboard = returnTrue

    def updateTimer(self, elapsedTime: str, percent: int, mode: str) -> None:
        """Update the status of the timer
        Change the text control and the progress bar to reflect the changes
        Parameters:
        - elapsedTime: elapsed time in string
        percent: percentage of time elapsed
        - mode: current mode i.e. break / focus
        """
        self.timerText.SetValue(f"{mode.title()} - {elapsedTime}")
        self.timerProgress.SetValue(percent)

    def reset(self) -> None:
        """Resets the view"""
        self.timerText.SetValue('00:00:00')
        self.timerProgress.SetValue(0)
