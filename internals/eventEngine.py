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
   '''
   The EventEngine Class is responsible for treating all incomming events
   '''

   def __init__(self):
      '''
      Constructor
      '''

      threading.Thread.__init__(self)
      self.eventqueue = Queue.Queue()
      self.finished = 0
      self.PluginManager = plugin_mgr.PluginManagerClass(self)


   def getPluginManager(self):
      '''
      Returns the PluginManager
      '''

      return self.PluginManager


   def post(self,event):
      '''
      Posts an event to the EventEngine's queue to be processed

      @param task: The event
      @type task: A task object
      '''

      self.eventqueue.put(event)

      logging.debug('(in EventEngine) posting event %s' %(event.name))


   def stopengine(self):
      '''
      Stops the engine
      '''

      self.finished = 1

      logging.warning("SETTING TO STOP")


   def run(self):
      '''
      Run the EventEngine
      '''

      logging.warning("STARTING")
      
      while(not self.finished):
         
         # Get the next event from the queue
         nextEvent = self.eventqueue.get() #python's bug: can't be killed by Ctrl+C
         logging.debug("get event %s" %(nextEvent.name))
         
         # TODO: clarify -> What are these newTasks?
         # These newTasks contains all actions we have to execute, with the event parameter names bindings
         newTasks = list()
         
         # Get users that might be interested in this event
         for u in userModule.getUsers():
            
            logging.warning("eventEngine sees user %s" %(u.name))
            
            ep = u.getProfileByEvent(nextEvent)
            
            if (ep != None):
               logging.debug("(eventEngine) user's %s profile for event %s has actions : " %(u.name, nextEvent.name))
               for b in ep.getBindings():
                  logging.debug(b.action.name)
                  
                  # TODO: define policy
                  #   should we execute each action for each user?
                  #   some (at least internals) actions need to be executed only once... 
                  #   not on a per-user basis (typically user creation...)
                  
               newTasks.extend(ep.getBindings())

            else:
               logging.error("BEWARE! user %s has no EventProfile attached!!" %(u.name))
         
         #Optional, but at this point the engine can add info on users or whatever state it wants and give that to the action
         nextEvent.actionArgs.update({'testArg':"fromEngine"}) 
         
         if (len(newTasks) <= 0):
            logging.warning("no action to execute for event %s, ignoring it" %(nextEvent.name))
         
         for t in newTasks:
            logging.debug("eventEngine executing %s for event %s (event args are %s)" %(t.action.name, nextEvent.name, nextEvent.actionArgs))
            actionArgs = copy(nextEvent.actionArgs) #construct a copy of args from event
            actionArgs[t.actionArgument] = nextEvent.actionArgs[t.eventArgument] #apply our bindings in the copy
            t(actionArgs)
            t.treated = 1
      
      time.sleep(5) #TODO: remove ugly sleep and actually wait on synced plugins (eg. voice) to end processing
      logging.warning("STOPPING")


# To be able to instantiate a sole EventEngine we need to do some dirty tricks:
# Singleton methodology...
class TheEventEngine(EventEngine):

   __instance = None

   def __new__(cls):
      if cls.__instance == None:
         cls.__instance = EventEngine.__new__(cls)
      return cls.__instance
