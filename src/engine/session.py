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

    def start(self):
        """Starts a full pomodoro session"""
        log.debug("Starting a new pomodoro session")
        try:
            for i in range(self.fullCircle):
                self.circle()
        except TimerStopError:
            log.debug("caugth TimerStop in start")
            return

    def circle(self):
        """Runs a full pomodoro circle"""
        log.debug("Starting a pomodoro circle")
        self.focus()
        self.takeBreak()

    def takeBreak(self):
        """Runs the timer for `break` time duration"""
        log.debug("Starting the take break timer...")
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
            # todo: remove this when you remove self.start and self.circle
            raise(TimerStopError("catch me in start"))

        pub.sendMessage('timerDone')
        if lastCircle:
            pub.sendMessage('sessionFinished')

    def focus(self):
        """Runs the timer for `focus` time duration"""
        log.debug("Starting the focus timer...")
        self.circleNo += 1  # New circle
        try:
                for elapsedTime, percentage in Timer(seconds=self.focusTime,
                                                     event=self.event):
                    pub.sendMessage('updateTimer', time=elapsedTime,
                                percent=percentage, mode='focus')
        except TimerStopError:
            log.debug("Timer stopped in focus mode")
            pub.sendMessage('timerStopped')
            # todo: remove this when you remove self.start and self.circle
            raise(TimerStopError("catch me in start"))

        pub.sendMessage('timerDone')
