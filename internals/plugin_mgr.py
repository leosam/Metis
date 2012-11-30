#!/usr/bin/python
import logging
import inspect
import copy
import plugin_def
from userModule import *

class PluginManagerClass:
   def __init__(self, evtmgr=None):
      self.eventManager = evtmgr
      self.pluginList = list()

   def post(self, event):
      logging.debug('(in pluginManager) posting event %s ' %(event.name))
      self.eventManager.post(event)

   def registerPlugin(self, plugin):
      self.pluginList.append(plugin)
      #TODO: choose default policy
      # wether or not we should bind all actions for each event inside a plugin
      # by default, as a start (so it does something when you add a plugin)
      plugin.manager = self
      plugin.registered = 1
      plugin.start() #don't forget to start the plugin's thread

   def getAvailableActions(self):
      actions = list()
      for p in self.pluginList:
         for a in p.getActionList():
            actions.append(a)
      return actions

   def getActionByName(self, actionName):
      for action in self.getAvailableActions():
         if (action.name == actionName):
            return action
      return None

   def getAvailableEvents(self):
      events = list()
      for p in self.pluginList:
         for e in p.getEventList():
            events.append(e)
      return events

   def getEventByName(self, eventName):
      for event in self.getAvailableEvents():
         if (event.name == eventName):
            return event
      return None

