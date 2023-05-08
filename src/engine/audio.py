# -*- coding: utf-8 -*-
"""This module manages the alarm that is played after a timer is done"""

import vlc
from logging import getLogger
import os


log = getLogger(__name__)


class Audio:
    """Plays an audio"""

    def __init__(self) -> None:
        """Initialize the object"""
        log.debug("initializing Audio")
        # initialize vlc instance, media player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def playAudio(self, path: str) -> None:
        """Plays the audio
        Parameter:
        - path: path to audio file
        """
        if not os.path.exists(path):
            log.debug(f"current path: {os.getcwd()}")
            raise(ValueError(f"Couldn't find the file {path}"))

        # create media object
        audio = self.instance.media_new(path)

        # play
        self.player.set_media(audio)
        self.player.play()
        log.debug(f"Playing audio {path}")
