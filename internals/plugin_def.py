#!/usr/bin/python

import threading
import logging
import inspect
import copy
import action_def

class Plugin(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.events = list()
        self.actions = list()
	
    def getEventList(self):
        return self.events
    def addEvent(self, event):
        self.getEventList().append(event)
    def getActionList(self):
        return self.actions
    def addAction(self, action):
        self.getActionList().append(action)
	
    def post(self, event):
       if (self.registered):
          logging.warning('plugin '+self.name+"posting event "+event.name)
          self.manager.post(event)
       else:
          logging.warning('plugin '+self.name+"can't post "+event.name+" because it's not registered")

    def run(self):
        logging.debug("starting plugin thread")

