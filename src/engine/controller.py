# -*- coding: utf-8 -*-
"""
This is the heart of the engine.
It controlls the Session object and binds pubsub events
"""

from pubsub import pub
from logging import getLogger
from threading import Thread, Event

from .session import Session
from .messenger import REPMessenger, PUBMessenger


log = getLogger(__name__)


class Controller:
    """Controlls what the engine does.
    who handles what
    """

    def __init__(self):
        """Initialize all the necessary objects and bind pubsub events"""
        log.debug("Initializing controller")
        self.sessionThread = None
        self.supportedRequests = {
                'start': self.startReq,
                'exit': self.exitReq,
                }
        self.pubMessenger = PUBMessenger()
        self.reqThreadEvent = Event()
        self.repMessengerThread = Thread(
                target=REPMessenger, daemon=True, args=(self.reqThreadEvent, ))
        self.repMessengerThread.start()
        self.session = Session()

        self.bindPubsub()

        self.repMessengerThread.join()

    def bindPubsub(self):
        """Bind all pub sub events."""
        pub.subscribe(self.updateTimer, "updateTimer")
        pub.subscribe(self.handleRequest, 'handleRequest')
        pub.subscribe(self.sessionFinished, 'sessionFinished')

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

    def updateTimer(self, time: str, percent: int):
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
        self.reqThreadEvent.set()
        reply = {
                'type': 'success',
                'requestName': 'exit',
            }
        pub.sendMessage('sendRep', reply=reply)

    def sessionFinished(self) -> None:
        """Deletes the session thread and tells view a session have finished"""
        self.sessionThread = None

        message = {
                'topic': 'sessionFinished',
                }
        pub.sendMessage('sendPubsub', message=message)
