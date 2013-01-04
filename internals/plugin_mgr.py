#!/usr/bin/python
import logging
import inspect
import copy
import threading
import plugin_def
import userModule 

class PluginManagerClass:
   def __init__(self):
      self.pluginList = list()
      self.perUserPlugins = list()
      self.globalPlugins = list()
      self.userThreads = dict()

   def registerPlugin(self, plugin):
      self.pluginList.append(plugin)
      plugin.manager = self
      plugin.registered = 1
      plugin.conf = plugin_def.getPluginConf(plugin.module)
      if (plugin.name != plugin.conf['PLUGIN_NAME']):
         logging.error("plugin names differ : %s != %s (should be the same)" %(plugin.name, plugin.conf['PLUGIN_NAME']))
      try: 
         if (plugin.conf['PLUGIN_USER_POLICY'] == 'perUser'):
            self.perUserPlugins.append(plugin)
         else:
            # assume PLUGIN_USER_POLICY == 'global' as default
            self.globalPlugins.append(plugin)
      except KeyError:
         self.globalPlugins.append(plugin)

   def startPlugins(self):
      for p in self.globalPlugins:
         p.start() #simply start the only one plugin's thread
      for p in self.perUserPlugins:
         for u in userModule.getUsers():
            t = copy.copy(p)
            threading.Thread.__init__(t)
            self.userThreads[u.name] = t
            t.user = u
            t.start()

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

   def getPluginByName(self, pluginName):
      for plugin in self.pluginList:
         if (plugin.name == pluginName):
            return plugin
      return None

# To be able to instantiate a sole PluginManagerClass we need to do some dirty tricks:
# Singleton methodology...
class ThePluginManager(PluginManagerClass):

   __instance = PluginManagerClass()

   def __init__(self):
      self.__dict__ = ThePluginManager.__instance.__dict__
      self.__class__ = ThePluginManager.__instance.__class__

