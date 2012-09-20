#!/usr/bin/python

import logging
import inspect
import copy
from plugin_def import *
from action_def import *


class builtinEvent(Event):
   def __init__(self, type="builtinEventType", name="builtinEvent"):
      super(builtinEvent,self).__init__(type, name)


class builtinAction(Action):
   def __init__(self, builtinPlugin, type="builtinAction", name="noname", plugin=None):
      if (plugin == None):
         plugin = builtinPlugin 
      super(builtinAction,self).__init__(type, name, plugin)
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

   
   def post(self, event):
      logging.warning("Posting from builtinPlugin");
      super(builtinPlugin, self).post(event)
