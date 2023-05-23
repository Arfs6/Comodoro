# -*- coding: utf-8 -*-
"""
This is the heart of the engine.
It controlls the Session object and binds pubsub events
"""

from pubsub import pub
from logging import getLogger
from threading import Thread, Event
from typing import Union, Dict

from config import config
from .audio import Audio
from .messenger import REPMessenger, PUBMessenger
from .session import Session


log = getLogger(__name__)


class Controller:
    """Controlls what the engine does.
    who handles what
    """

    def __init__(self):
        """Initialize all the necessary objects and bind pubsub events"""
        log.debug("Initializing controller")
        # initialize messengers
        self.supportedRequests = {
                'start': self.startReq,
                'exit': self.exitReq,
                'stop': self.stopReq,
                }
        self.reqThreadEvent = Event()
        self.repMessengerThread = Thread(
                target=REPMessenger, daemon=True, args=(self.reqThreadEvent, ))
        self.repMessengerThread.start()
        self.pubMessenger = PUBMessenger()

        # session
        self.sessionThread: Union[None, Thread] = None
        self.sessionEvent = Event()
        self.session = Session(self.sessionEvent)

        self.audio = Audio()

        self.subscribePubsub()

        self.repMessengerThread.join()

    def subscribePubsub(self):
        """Bind all pub sub events."""
        pub.subscribe(self.updateTimer, "updateTimer")
        pub.subscribe(self.handleRequest, 'handleRequest')
        pub.subscribe(self.sessionFinished, 'sessionFinished')
        pub.subscribe(self.timerDone, 'timerDone')
        pub.subscribe(self.timerStopped, 'timerStopped')

    def handleRequest(self, request: dict):
        """Handles the request by sending it to the appropriate method
        Parameter:
        - request: request message
        """
        requestType = request.get('type', None)
        if not requestType:
            log.debug("No 'type' key in request")
            reply = {
                    'type': 'error',
                    'info': 'No `type` field'
                    }
            pub.sendMessage('sendRep', reply=reply)
            return
        elif requestType not in self.supportedRequests:
            log.debug(f"An unsupported request was sent: {requestType}")
            reply = {
                    'type': 'error',
                    'info': f'unsupported type <{requestType}>'
                    }
            pub.sendMessage('sendRep', reply=reply)
            return

        self.supportedRequests[requestType](request)

    def updateTimer(self, time: str, percent: int, mode: str) -> None:
        """Sends the updated time
        Using the pubsub method
        parameters:
        - time: elapsed time, in format `hh:mm:ss`
        -percent: percent of time elapsed
        """
        message: dict = {
             'topic': 'updateTimer',
             'elapsedTime': time,
             'percent': percent,
             'mode': mode,
                }
        pub.sendMessage('sendPubsub', message=message)

    def startReq(self, request: dict):
        """Starts the timer
        Parameter:
            - request: request sent by view
        """
        reply = {
                'type': 'success',
                'requestName': 'start',
                }
        if self.sessionThread:
            pub.sendMessage('sendRep', reply=reply)
            return
        self.sessionThread = Thread(target=self.session.start, daemon=True)
        self.sessionThread.start()
        pub.sendMessage('sendRep', reply=reply)

    def exitReq(self, request: dict):
        """Exits the controller
        The only thing stopping the Controller from finishing is
        self.reqMessengerThread. So, stopping it will stop all the daemon
        thread depending on this thread
        Parameter:
        - request: request dictionary
        """
        reply = {
                'type': 'success',
                'requestName': 'exit',
            }
        pub.sendMessage('sendRep', reply=reply)
        self.reqThreadEvent.set()

    def sessionFinished(self) -> None:
        """Tells view a session have finished"""
        message = {
                'topic': 'sessionFinished',
                }
        pub.sendMessage('sendPubsub', message=message)

    def timerDone(self, mode: str) -> None:
        """Removes session thread and tells user timer is done
        Parameter:
        - mode: Which mode is finished
        """
        log.debug(f"{mode} timer done")
        self.sessionThread = None
        self.audio.playAudio(config.audio_timer)
        message = {
                'topic': 'timerDone',
                'mode': mode,
                }
        pub.sendMessage('sendPubsub', message=message)

    def stopReq(self, request: dict) -> None:
        """Stop the timer and session.
        Parameter:
         - request: the request dictionary
        """
        if not self.sessionThread:
            reply = {
                    'type': 'stop',
                    'status': 'stopped',
                    }
            pub.sendMessage('sendRep', reply=reply)
            return

        self.sessionEvent.set()
        if self.sessionThread:
            # Wait for session thread to finish
            self.sessionThread.join()

        reply: Dict[str, str] = {
                'type': 'success',
                'requestName': 'stop',
                }
        pub.sendMessage('sendRep', reply=reply)
        message: dict= {
                'topic': 'timerStopped',
                }
        pub.sendMessage('sendPubsub', message=message)

    def timerStopped(self):
        """Tell view timer has stopped and delete session thread.
        This method is called when view request to stop timer. `self.stopReq`.
        """
        self.sessionThread = None
        self.sessionEvent.clear()
