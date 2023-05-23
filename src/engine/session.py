# -*- coding: utf-8 -*-
"""
This module defines the Session class
"""

from pubsub import pub
import threading
from logging import getLogger

from errors import TimerStopError
from .timer import Timer
from config import config


log = getLogger(__name__)


class Session:
    """Represents a full pomodoro session"""

    def __init__(self, event: threading.Event) -> None:
        """Initialize Session attributes"""
        log.debug("Initializing Session object")
        self.event = event
        self.circleNo: int = 0
        self.focusTime: int = config.timer_focus
        self.shortBreakTime: int = config.timer_shortBreak
        self.longBreakTime: int = config.timer_longBreak
        self.fullCircle: int = config.timer_fullCircle
        self.isFocus: bool = False  # if the last mode finished is focus

    def start(self):
        """Start the next timer"""
        log.debug("Starting the next timer...")
        if self.isFocus:
            self.takeBreak()
        else:
            self.focus()

    def takeBreak(self):
        """Runs the timer for `break` time duration"""
        log.debug("Starting the take break timer...")
        self.isFocus = False
        lastCircle: bool = self.circleNo == self.fullCircle
        if not lastCircle:
            # short break
            breakTime = self.shortBreakTime
        else:
            breakTime = self.longBreakTime

        try:
            for elapsedTime, percentage in Timer(seconds=breakTime,
                                                 event=self.event):
                pub.sendMessage('updateTimer', time=elapsedTime,
                                percent=percentage, mode='break')
        except TimerStopError:
            log.debug("Timer stopped in break mode")
            pub.sendMessage('timerStopped')
            return

        if lastCircle:
            pub.sendMessage('timerDone', mode='longBreak')
            pub.sendMessage('sessionFinished')
        else:
            pub.sendMessage('timerDone', mode='shortBreak')

    def focus(self):
        """Runs the timer for `focus` time duration"""
        log.debug("Starting the focus timer...")
        self.isFocus = True
        self.circleNo += 1  # New circle
        try:
                for elapsedTime, percentage in Timer(seconds=self.focusTime,
                                                     event=self.event):
                    pub.sendMessage('updateTimer', time=elapsedTime,
                                percent=percentage, mode='focus')
        except TimerStopError:
            log.debug("Timer stopped in focus mode")
            pub.sendMessage('timerStopped')
            return

        pub.sendMessage('timerDone', mode='focus')
