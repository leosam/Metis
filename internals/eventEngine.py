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
import eventProfileBindings

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
   def updateArgs(self, args, bindings, event):
      for b in bindings:
         args[b.actionArgument] = event.eventArgs[b.eventArgument]


   def run(self):
      '''
      Run the EventEngine
      '''

      logging.warning("STARTING")
      
      while(not self.finished):
         
         # Get the next event from the queue
         nextEvent = self.eventqueue.get() #python's bug: can't be killed by Ctrl+C
         logging.debug("get event %s" %(nextEvent.name))
         
         # Temporarily Store actions to execute
         actionsToExec = list()
         
         #Optional, but at this point the engine can add info on users or whatever state it wants and give that to the action
         nextEvent.eventArgs.update({'testArg':"fromEngine"}) 
         
         # Get users that might be interested in this event
         for u in userModule.getUsers():
            
            logging.warning("eventEngine sees user %s" %(u.name))
            
            ep = u.getProfileByEvent(nextEvent)
            
            if (ep != None):
               logging.debug("(eventEngine) user's %s profile for event %s has actions : " %(u.name, nextEvent.name))
               for action in ep.getActions():
                  newArgs = copy.copy(nextEvent.eventArgs) #copy args from event before modifying them
                  self.updateArgs(newArgs, ep.getBindingsForAction(action), nextEvent)
                  actionsToExec.append([action, newArgs])

            else:
               logging.error("BEWARE! user %s has no EventProfile attached!!" %(u.name))
         
         if (len(actionsToExec) <= 0):
            logging.warning("no action to execute for event %s, ignoring it" %(nextEvent.name))
         
         for a,args in actionsToExec:
            a(args)
            a.treated = 1
      
      time.sleep(5) #TODO: remove ugly sleep and actually wait on synced plugins (eg. voice) to end processing, when needed
      logging.warning("STOPPING")


# To be able to instantiate a sole EventEngine we need to do some dirty tricks:
# Singleton methodology...
class TheEventEngine(EventEngine):

   __instance = EventEngine()

   def __init__(self):
      self.__dict__ = TheEventEngine.__instance.__dict__
      self.__class__ = TheEventEngine.__instance.__class__

