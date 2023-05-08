#-*- coding: utf-8 -*-
"""
All configuration / settings related codes are here
"""

from configobj import ConfigObj
from configobj.validate import Validator

import paths


config = {
    'shortBreak': 2,
    'focus': 5,
    'maxCircles': 4,
    'longBreak': 5,
}

class Config:
    """This is a wrapper arround the main config object
    To access configs, use the dot `.` notation.
    This is to reduce Possible errors with typos
    """

    def __init__(self) -> None:
        """Initialize the main config object"""
        configSpec = ConfigObj(
                infile=paths.configPath(isspec=True),
                encoding='utf-8',
                indent_type='\t',
                list_values=False
                )

        self.config = ConfigObj(
                infile=paths.configPath(),
                encoding='utf-8',
                indent_type='\t',
                configspec=configSpec
                )

        # Validate config file
        validator = Validator()
        self.config.validate(validator, copy=True)

    @property
    def timer_shortBreak(self) -> int:
        """Break in timer section"""
        return self.config['timer']['shortBreak']

    @timer_shortBreak.setter
    def timer_shortBreak(self, value: int) -> None:
        """Saves the timer short break time"""
        self.config['timer']['shortBreak'] = value
        self.config.write()

    @property
    def timer_longBreak(self) -> int:
        """Long break after last focus in a session"""
        return self.config['timer']['longBreak']

    @timer_longBreak.setter
    def timer_longBreak(self, value: int) -> None:
        """Setter method for long break"""
        self.config['timer']['longBreak'] = value
        self.config.write()

    @property
    def timer_focus(self) -> int:
        """The time for focusing"""
        return self.config['timer']['focus']

    @timer_focus.setter
    def timer_focus(self, value: int) -> None:
        """setter method for focus"""
        self.config['timer']['focus'] = value
        self.config.write()

    @property
    def timer_fullCircle(self) -> int:
        """Number of circles that makes up a full pomodoro session"""
        return self.config['timer']['fullCircle']

    @timer_fullCircle.setter
    def timer_fullCircle(self, value: int) -> None:
        """setter method for full circle"""
        self.config['timer']['fullCircle'] = value
        self.config.write()

    @property
    def messenger_REQPort(self) -> int:
        """The port to use to communicate using the send / receive method"""
        return self.config['messenger']['REQPort']

    @messenger_REQPort.setter
    def messenger_REQPort(self, value: int) -> None:
        """setter method for REQPort"""
        self.config['messenger']['REQPort'] = value
        self.config.write()

    @property
    def messenger_PUBPort(self) -> int:
        """The port to communicate using pubsub method"""
        return self.config['messenger']['PUBPort']

    @messenger_PUBPort.setter
    def messenger_PUBPort(self, value: int) -> None:
        """setter method for PUBPort"""
        self.config['messenger']['PUBPort'] = value
        self.config.write()

    @property
    def messenger_timeout(self) -> int:
        """Timeout for messengers to stop trying and alert the user"""
        return self.config['messenger']['timeout']

    @messenger_timeout.setter
    def messenger_timeout(self, value: int) -> None:
        """Setter method for messenger_timeout
        Parameter:
        - value: value to set
        """
        self.config['messenger']['timeout'] = value
        self.config.write()

    @property
    def audio_timer(self) -> str:
        """The audio to play when a timer is done"""
        return self.config['audio']['timer']

    @audio_timer.setter
    def audio_timer(self, path: str) -> None:
        """setter method for audio_timer"""
        self.config['audio']['timer'] = path
        self.config.write()


config = Config()  # This object should be used for accessing configs
