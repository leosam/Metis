#!/usr/bin/python

import logging
import inspect
import copy
from plugin_def import *
from action_def import *


class builtinEvent(Event):
   def __init__(self):
      super(builtinEvent,self).__init__("builtinEventType", "builtinEvent")


class builtinAction(Action):
   def __init__(self, builtinPlugin):
      super(builtinAction,self).__init__("builtinAction", "noname", builtinPlugin)
   def __call__(self, args={}):
      logging.warning("in builtinAction! %s", args);


class triggerEvent(builtinAction):
   def __init__(self, builtinPlugin):
      super(triggerEvent,self).__init__(builtinPlugin)
      self.name = "triggerEvent"
   def __call__(self, args={}):
      try:
         self.event = args['eventClass']()
      except KeyError:
         logging.error("triggerEvent called with no eventClass. Abort.")
      else:
         try:
            self.event.actionArgs = args['actionArgs']
         except:
            self.event.actionArgs = {}
         logging.warning("triggering event %s", args);
         self.post(event)



class builtinPlugin(Plugin):
   
   def __init__(self):
      super(builtinPlugin,self).__init__();
      self.addAction(builtinAction(self))
      self.addEvent(builtinEvent())
      self.addAction(triggerEvent(self))

