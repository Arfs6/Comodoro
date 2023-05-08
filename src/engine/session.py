# -*- coding: utf-8 -*-
"""
This module defines the Session class
"""

from pubsub import pub

from logging import getLogger

from .timer import Timer
from config import config


log = getLogger(__name__)


class Session:
    """Represents a full pomodoro session"""

    def __init__(self):
        """Initialize Session attributes"""
        log.debug("Initializing Session object")
        self.circleNo: int = 0
        self.focusTime: int = config.timer_focus
        self.shortBreakTime: int = config.timer_shortBreak
        self.longBreakTime: int = config.timer_longBreak
        self.fullCircle: int = config.timer_fullCircle

    def start(self):
        """Starts a full pomodoro session"""
        log.debug("Starting a new pomodoro session")
        for i in range(self.fullCircle):
            self.circle()

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

        for elapsedTime, percentage in Timer(seconds=breakTime):
            pub.sendMessage('updateTimer', time=elapsedTime, percent=percentage)

        pub.sendMessage('timerDone')
        if lastCircle:
            pub.sendMessage('sessionFinished')

    def focus(self):
        """Runs the timer for `focus` time duration"""
        log.debug("Starting the focus timer...")
        self.circleNo += 1  # New circle
        for elapsedTime, percentage in Timer(seconds=self.focusTime):
            pub.sendMessage('updateTimer', time=elapsedTime, percent=percentage)

        pub.sendMessage('timerDone')
