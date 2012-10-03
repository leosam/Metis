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
import plugin_def
import userModule
import plugin_mgr

class EventEngine(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
      self.eventqueue = Queue.Queue()
      self.finished = 0
      self.PluginManager = plugin_mgr.PluginManagerClass(self)

   def getPluginManager(self):
      return self.PluginManager

   def post(self,task):
      logging.debug('(in EventEngine) posting event %s' %(task.name))
      self.eventqueue.put(task)

   def stopengine(self):
      logging.warning("SETTING TO STOP")
      self.finished = 1

   def run(self):
      logging.warning("STARTING")
      while(not self.finished):
         newEvent = self.eventqueue.get() #python's bug: can't be killed by Ctrl+C
         logging.debug("get event %s" %(newEvent.name))
         newTasks = list()
         for u in userModule.getUsers():
            logging.warning("eventEngine sees user %s" %(u.name))
            ep = u.getProfileByEvent(newEvent)
            if (ep != None):
               logging.debug("(eventEngine) user's %s profile for event %s has actions : " %(u.name, newEvent.name))
               for a in ep.getActions():
                  logging.debug(a.name)
               #TOTO: define policy
               # should we execute each action for each user?
               # some (at least internals) actions need to be executed only once... not on a per-user basis (typically user creation...)
               newTasks.extend(ep.getActions())
            else:
               logging.error("BEWARE! user %s has no EventProfile attached!!" %(u.name))
         newEvent.actionArgs.update({'testArg':"fromEngine"}) #optional, but the engine could add info on users or whatever state it wants and give that to the action
         if (len(newTasks) <= 0):
            logging.warning("no action to execute for event %s" %(newEvent.name))
         for t in newTasks:
            logging.debug("eventEngine executing %s for event %s (args are %s)" %(t.name, newEvent.name, newEvent.actionArgs))
            t(newEvent.actionArgs)
            t.treated = 1
      
      time.sleep(5) #TODO: remove ugly sleep and actually wait on all plugins to stop instead
      logging.warning("STOPPING")

def endtask(**args):
   args['engine'].post(action_def.Action(args['engine'].stopengine))

def dummytask(**args):
   logging.warning("DUMMY TASK, args: %s" %(str(args)))


