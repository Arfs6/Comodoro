# -*- coding: utf-8 -*-
"""The messenger manages communication between the gui, cli and the engine
"""

import zmq
from logging import getLogger
from pubsub import pub
import threading

from config import config


log = getLogger(__name__)


class PUBMessenger:
    """This is the pubsub messenger class"""

    def __init__(self):
        """Initialize the pubsub socket and subscribe for pubsub messeges"""
        log.debug("initializing pubsub socket")
        self.context = zmq.Context()
        self.pubSocket = self.context.socket(zmq.PUB)
        self.pubSocket.bind(
                f"tcp://*:{config.messenger_PUBPort}"
                )

        # subscribe for pubsub messages
        pub.subscribe(self.sendPubsub, 'sendPubsub')

    def sendPubsub(self, message: dict) -> None:
        """Send pub-sub message to subscribers using the pub sub socket
        Parameter:
        - message: The message to send.
        """
        log.debug(f"sending pubsub message: {message}")
        self.pubSocket.send_json(message)


class REPMessenger:
    """Represents the reply messenger
    It should be on a different thread
    """

    def __init__(self, event: threading.Event):
        """Initialize the reply socket and start listening"""
        log.debug("initializing reply socket")
        self.event =event
        self.context = zmq.Context()
        self.repSocket = self.context.socket(zmq.REP)
        bindArg = f"tcp://*:{config.messenger_REQPort}"
        self.repSocket.bind(bindArg)
        log.debug(f"rep socket binded: {bindArg}")

        # subscribe for pubsub messeges
        pub.subscribe(self.sendRep, 'sendRep')
        self.listenAndRespond()

    def listenAndRespond(self):
        """Listens for messages from view and send response
        The response will be gotten by sending a pub sub message to the
        controller
        """
        log.debug("listening for requests from view ...")
        log.debug(f"event.is_set() := {self.event.is_set()}")
        while not self.event.is_set():
            # listen
            # if self.repSocket.poll(timeout=1000, flags=zmq.POLLIN) == 0:
                # continue
            request = self.repSocket.recv_json()
            log.debug(f"Recieved request from view via rep socket: {request}")
            # respond
            pub.sendMessage('handleRequest', request=request )

        log.debug(f"Done listening for requests")

    def sendRep(self, reply: dict):
        """Send respond to the view"""
        log.debug(f"Sending reply to view: {reply}")
        self.repSocket.send_json(reply)
