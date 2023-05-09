# -*- coding: utf-8 -*-

"""
This is the controller for the gui view
"""

import wx
from logging import getLogger
from pubsub import pub
from threading import Thread, Event
from typing import Callable, Dict

from .mainview import AppFrame
from .messenger import REQMessenger, SUBMessenger


log = getLogger(__name__)


class Controller:
    """Controls the main view of the aplication
    """

    def __init__(self):
        """Make gui ready by initializing messengers and gui"""
        self.view = AppFrame()
        # initialize messengers
        self.subThreadEvent = Event()
        self.subMessengerThread = Thread(
                target=SUBMessenger, daemon=True, args=(self.subThreadEvent, )
                )
        self.subMessengerThread.start()

        self.initAttrs()
        self.bindGUIElements()
        self.subscribePubsubEvents()

        self.view.Show()
        log.debug("Called Show method of AppFrame")
        # self.subMessengerThread.join()

    def initAttrs(self):
        """Initialize common attributes"""
        self.supportedTopics: Dict[str, Callable[[dict], None]] = {
                'updateTimer': self.updateTimer,
                'sessionFinished': self.sessionFinished,
                }

        # supported replies
        self.supportedReplies: Dict[str, Callable[[dict], None]] = {
                'success': self.successRep,
                'error': self.errorRep,
                }

    def subscribePubsubEvents(self):
        """Subscribe for pubsub events"""
        log.debug("subscribing for pubsub events")
        pub.subscribe(self.handleReply, 'handleReply')
        pub.subscribe(self.handleSubMessages, 'recvSub')
        pub.subscribe(self.close, 'exit')
        pub.subscribe(REQMessenger, 'sendReq')

    def bindGUIElements(self):
        """Bind GUI elements to the appropriate handlers"""
        log.debug("binding gui elements")
        self.view.mainBtn.Bind(wx.EVT_BUTTON, self.onMainBtn)
        self.view.settingsBtn.Bind(wx.EVT_BUTTON, self.notImplemented)
        self.view.helpBtn.Bind(wx.EVT_BUTTON, self.notImplemented)

    def handleReply(self, reply: dict):
        """Handle replies send by engine
        Parameter:
        - reply: a dictionary containing data returned by engine
        """
        replyType = reply.get('type')
        if not replyType:
            log.error("No `type` field in reply dictionary")
        elif replyType not in self.supportedReplies:
            log.error(f"An unsupported reply was recieved: {replyType}")
        else:
            self.supportedReplies[replyType](reply)

    def handleSubMessages(self, message: dict):
        """Handles pub / sub mesages sent by engine
        Parameter:
        - message: message sent by engine using pubsub socket
        """
        topic = message.get('topic')
        if not topic:
            log.debug(
            f"Message sent by engine via pubsub has no topic: {message}")
        elif topic not in self.supportedTopics:
            log.debug(f"An unsupported topic was sent via pubsub socket: {topic}")

        self.supportedTopics[topic](message)

    def onMainBtn(self, event):
        """Handle the main button click event"""
        log.debug("Main button pressed")
        request = {
                'type': self.view.mainBtn.GetLabel().lower()
                }
        pub.sendMessage('sendReq', request=request)

    def notImplemented(self, event):
        """ Display a dialog telling the user this feature hasn't been
        implemented yet
        """
        log.debug("An unimplemented feature was pressed")
        dlg = wx.MessageDialog(self.view,
                               "This feature hasn't been implemented yet",
                               "Not implemented",
                               wx.OK).ShowModal()
        dlg.Destroy()

    def updateTimer(self, message: dict):
        """Update the timer text box and progress bar
        Parameter:
        - message: pubsub message sent
        """
        log.debug(f"updating timer with: {message}")
        self.view.updateTimer(message['elapsedTime'], message['percent'],
                              message['mode'])

    def successRep(self, reply: dict):
        """Successful request, do nothing
        Parameter:
        - reply: reply dictionary
        """
        log.debug(
                f"The request {reply['requestName']} was successful"
                )

    def errorRep(self, reply:dict ):
        """A request was wrong, do nothing
        Parameter:
        - reply: reply dictionary
        """
        log.error(
                f"A request returned an error\n"
                f"info: {reply['info']}"
                )

    def close(self):
        """Perform clean up tasks and exits"""
        # stop listening for pubsub messages
        self.subThreadEvent.set()

        # send exit request to engine
        request = {
                'type': 'exit',
                }
        pub.sendMessage('sendReq', request=request)

    def sessionFinished(self, message: dict) -> None:
        """A message have finished. Reset the view
        Parameter:
        - message: the message dictionary
        """
        self.view.reset()
