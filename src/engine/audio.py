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
        self.instance: vlc.Instance = vlc.Instance()
        self.player: vlc.MediaPlayer = self.instance.media_player_new()

    def playAudio(self, path: str) -> None:
        """Plays the audio
        Parameter:
        - path: path to audio file
        """
        log.debug(f"Playing audio ({path})")
        if not os.path.exists(path):
            log.error(f"Couldn't find audio file to play.")
            return

        # create media object
        audio: vlc.Media = self.instance.media_new(path)

        # play
        self.player.set_media(audio)
        self.player.play()
