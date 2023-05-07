#-*- coding: utf-8 -*-
"""
This module defines the Timer class.
"""

from time import sleep, time
import typing


class Timer:
    """
    This class represents a timer.
    """

    def __init__(self, hours=0, minutes=0, seconds=0):
        """Initialize the Timer object
        Parameters:
        - hours: Hours to sleep
        - minutes: Minutes to sleep
        - seconds: Seconds to sleep
        Start time for timer defaults to `0` when no arguments is passed
        """
        self.stopTime = hours * 3600 + minutes * 60 + seconds

    def __iter__(self):
        """Make the Timer itterable"""
        self.startTime = time()
        return self

    def __next__(self) -> typing.Tuple[str, int]:
        """Sleep for some mili seconds and return elapsed time
        Return: tuple: elapsed time, percentage
        """
        currentTime = time()
        if currentTime >= self.startTime + self.stopTime:
            raise StopIteration()
        sleep(0.25)
        elapsedTime = currentTime - self.startTime
        hours, rem = divmod(int(elapsedTime), 3600)
        mins, secs = divmod(rem, 60)
        percentage = int((elapsedTime / self.stopTime) * 100)
        return f"{hours:02d}:{mins:02d}:{secs:02d}", percentage
