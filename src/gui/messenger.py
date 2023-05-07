# -*- coding: utf-8 -*-
"""The messengers manages communication with the engine"""

import zmq
from zmq.utils.monitor import recv_monitor_message
from threading import Thread
from logging import getLogger
from pubsub import pub
from traceback import format_exc

from config import config


log = getLogger(__name__)


EVENT_MAP = {}
for name in dir(zmq):
    if name.startswith('EVENT_'):
        value = getattr(zmq, name)
        EVENT_MAP[value] = name

def eventMonitor(monitor: zmq.Socket) -> None:
    while monitor.poll():
        evt = {}
        mon_evt = recv_monitor_message(monitor)
        evt.update(mon_evt)
        evt['description'] = EVENT_MAP[evt['event']]
        log.debug(f"Event: {evt}")
        if evt['event'] == zmq.EVENT_MONITOR_STOPPED:
            break
    monitor.close()
    log.debug("event monitor thread done!")


class SUBMessenger:
    """This is the pubsub messenger class
    It subscribes for messages that updates the timer from the engine
    it should be on a different thread
    """

    def __init__(self, event):
        """Initialize the pubsub socket"""
        log.debug("initializing sub socket")
        self.event = event
        self.context = zmq.Context()
        self.subSocket = self.context.socket(zmq.SUB)
        monitor = self.subSocket.get_monitor_socket()
        t = Thread(target=eventMonitor, args=(monitor, ), daemon=True)
        t.start()
        self.subSocket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.subSocket.connect(
                f"tcp://localhost:{config.messenger_PUBPort}"
                )
        self.recvSub()

    def recvSub(self):
        """Receivs messages from engine"""
        log.debug("listening for pubsub messeges in socket")
        while not self.event.is_set():
            if self.subSocket.poll(timeout=config.messenger_timeout, flags=zmq.POLLIN) == 0:
                continue
            message = self.subSocket.recv_json()
            log.debug(f"Recieved pubsub message via sub socket: {message}")
            try:
                pub.sendMessage('recvSub', message=message)
            except Exception as E:
                log.error(format_exc())

        log.debug('Finished listening for pubsub messages')
        self.subSocket.disable_monitor()
        self.subSocket.close()
        self.context.term()


class _REQMessenger(Thread):
    """Represents the request messenger.
    Runs on a separate thread.
    """

    def __init__(self, request: dict):
        """Initialize the request socket
        Parameter:
        - request: the request dictionary
        """
        log.debug("initializing request socket")
        super().__init__(daemon=True)
        self.context = zmq.Context()
        self.reqSocket = self.context.socket(zmq.REQ)
        self.reqSocket.connect(
                f"tcp://localhost:{config.messenger_REQPort}"
                )
        self.poller = zmq.Poller()
        self.poller.register(self.reqSocket, zmq.POLLIN)
        self.request = request

        self.start()

    def run(self):
        """Send request to the engine and recieve reply"""
        # todo: catch errors when send fails and check zmq.LINGER flag
        log.debug(f"sending request to engine via req socket: {self.request}")
        self.reqSocket.send_json(self.request, flags=zmq.NOBLOCK)
        socks = dict(self.poller.poll(config.messenger_timeout))
        if socks and socks.get(self.reqSocket) == zmq.POLLIN:
            reply = self.reqSocket.recv_json()
            log.debug(f"Recieved reply from engine: {reply}")
            try:
                pub.sendMessage('handleReply', reply=reply)
            except Exception as E:
                log.error(format_exc())
        else:
            log.error("Timeout while recieving reply from engine")
        self.reqSocket.close()
        self.context.term()


def REQMessenger(request: dict):
    """This is a wrapper arround the REQMessenger class.
    It allows calling it with pub.sendMessage
    Parameter:
    - request: request argument of _REQMessenger
    """
    _REQMessenger(request)
