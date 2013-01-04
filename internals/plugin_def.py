#!/usr/bin/python

import threading
import logging
import inspect
import copy
import action_def
import pluginProfile
import eventEngine

def __isPluginPref(moduleMember):
   """
   Filter function used by getPluginPrefs
   """
   if (inspect.isclass(moduleMember)):
      return False
   return True

def getPluginPrefs(module):
   """
   Return the list of 'preferences' specified by the plugin defined in module
   """
   prefs = dict()
   for name,v in inspect.getmembers(module,__isPluginPref):
      if (name.startswith("PLUGIN_") ):
         prefs[name] = v
   return prefs

class Plugin(threading.Thread):
   def __init__(self, name):
      threading.Thread.__init__(self)
      self.events = list()
      self.actions = list()
      self.pluginProfiles = dict()
      self.name = name

   def getEventList(self):
      return self.events
   def addEvent(self, event):
      self.getEventList().append(event)

   def getActionList(self):
      return self.actions
   def addAction(self, action):
      self.getActionList().append(action)

   def addPluginProfile(self, user, prof):
      try:
         self.pluginProfiles[user.name] = prof
      except KeyError:
         #TODO
         logging.error("ERROR: PluginProfile merging not implemented yet!")
   def getPluginProfile(self, user):
      try:
         return self.pluginProfiles[user.name]
      except KeyError:
         return None

   def post(self, event):
      if (self.registered):
         logging.debug('(in plugin '+self.name+") posting event "+event.name+" for user "+self.user.name)
         event.recipient = self.user.name
         eventEngine.TheEventEngine().post(event)
      else:
         logging.warning('plugin '+self.name+"can't post "+event.name+" because it's not registered")

   def run(self):
      logging.debug("starting plugin thread")

