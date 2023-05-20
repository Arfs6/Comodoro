#-*- coding: utf-8 -*-
"""
This module defines the Timer class.
"""

from time import sleep, time
import typing
import threading

from errors import TimerStopError


class Timer:
    """
    This class represents a timer.
    """

    def __init__(self, event: threading.Event, seconds: int=0):
        """Initialize the Timer object
        Start time for timer defaults to `0` when no arguments is passed
        Parameters:
        - seconds: Seconds to sleep
        - event: event to set when timer should be stopped
        """
        self.stopTime = seconds
        self.event = event

    def __iter__(self):
        """Make the Timer itterable"""
        self.startTime = time()
        return self

    def __next__(self) -> typing.Tuple[str, int]:
        """Sleep for some mili seconds and return elapsed time
        Return: tuple: elapsed time, percentage
        """
        if self.event.is_set():
            raise(TimerStopError("Timer has been stopped"))
        currentTime = time()
        if currentTime >= self.startTime + self.stopTime:
            raise StopIteration()
        sleep(0.25)

        # incase event was set after sleeping
        if self.event.is_set():
            raise(TimerStopError("Timer has been stopped"))

        elapsedTime = currentTime - self.startTime
        hours, rem = divmod(int(elapsedTime), 3600)
        mins, secs = divmod(rem, 60)
        percentage = int((elapsedTime / self.stopTime) * 100)
        return f"{hours:02d}:{mins:02d}:{secs:02d}", percentage
