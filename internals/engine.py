#!/usr/bin/python
import threading
import os
#import festival
import time
import Queue
import logging
import inspect
import copy
import action_def
import plugin_mgr
import plugin_def
import user_def

class EventEngine(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
      self.eventqueue = Queue.Queue()
      self.finished = 0
      self.PluginManager = plugin_mgr.PluginManagerClass(self);

   def getPluginManager(self):
      return self.PluginManager

   def post(self,task):
      logging.warning('EventEngine posting event '+task.name)
      self.eventqueue.put(task)

   def stopengine(self):
      logging.warning("SETTING TO STOP")
      self.finished = 1

   def run(self):
#      logging.info("starting festival server")
#      self.festival = festival.FestivalWrapper()
#      self.festival.start()
      logging.warning("STARTING")
      while(not self.finished):
         newEvent = self.eventqueue.get() #python's bug: can't be killed by Ctrl+C
         logging.debug("get event %s", newEvent.name)
         newTasks = list()
         for u in user_def.getUsers():
            ep = u.getProfileByEvent(newEvent)
            newTasks.extend(ep.getActions())
         newEvent.actionArgs.update({'testArg':"fromEngine"}) #optional, but the engine could add info on users or whatever state it wants and give that to the action
         for t in newTasks:
            t(newEvent.actionArgs)
            t.treated = 1
      
      time.sleep(5); #TODO: remove ugly sleep and wait on all plugins to stop instead
      logging.warning("STOPPING")
#      self.festival.stop()

def endtask(**args):
   args['engine'].post(action_def.Action(args['engine'].stopengine));

def dummytask(**args):
   logging.warning("DUMMY TASK, args: %s", str(args))


