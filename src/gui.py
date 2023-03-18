# -*- coding: utf-8 -*-
"""
Defines Gui classes for the app
"""

import wx
from logging import getLogger
from winsound import Beep
import time
import threading

from app_info import appName


log = getLogger(__name__)


class Application(wx.App):
    def OnInit(self):
        """Initialize the application's wx.App"""
        log.debug('wx.App initialized')
        self.frame = AppFrame( self, appName)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

    def OnExceptionInMainLoop(self):
        """
        Handle unhandled exceptions during the main event loop.
        """
        print(log)
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

    def __init__(self, app, title):
        """Initialize app frame
        Parameter:
        -title: Title of the app
        """
        super().__init__(None, title=title)
        self.app = app
        self.InitUI()

    def InitUI(self):
        """Initialize the Main UI"""
        log.debug('Initializing the Main frame UI')
        panel = wx.Panel(self)
        self.button = wx.Button(panel, label="Start", pos=(50, 50))
        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked, self.button)

        self.timer_text = wx.StaticText(panel, label='00:00:00')
        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.timer_text.SetFont(font)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.button, wx.SizerFlags().Border(wx.ALL, 10).Center())
        sizer.Add(self.timer_text, wx.SizerFlags().Border(wx.ALL, 10).Center())
        panel.SetSizer(sizer)

        self.timerThread = None
        self.timer_start_time = None
        self.focusTime = 25 * 60
        self.restTime = 5 * 60
        self.timerDuration = self.focusTime

    def OnButtonClicked(self, *args, **kwargs):
        if self.timerThread is None:
            if self.timerDuration == self.focusTime:
                self.timerDuration = self.restTime
                self.button.SetLabel('Focus')
                log.debug('Main button set to Rest mode.')
            else:
                self.timerDuration = self.restTime
                self.button.SetLabel('Rest')
                log.debug('Main button set to Focus mode.')
            self.timer_start_time = time.time()
            self.timerThread = threading.Thread(target=self.run_timer)
            self.timerThread.start()
        # else:
        #     self.button.SetLabel('Start')
        #     self.timerThread.join()
        #     self.timerThread = None
        #     self.timer_text.SetLabel('00:00:00')

    def run_timer(self):
        while time.time() - self.timer_start_time < self.timerDuration:
            elapsed_time = time.time() - self.timer_start_time
            hours, remainder = divmod(int(elapsed_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
            wx.CallAfter(self.timer_text.SetLabel, time_str)
            time.sleep(1)
        wx.CallAfter(self.button.SetLabel, 'Start')
        for i in range(3):
            Beep(1000, 250)
        wx.CallAfter(self.timer_text.SetLabel, '00:00:00')
        self.timerThread = None
