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
         try:
            args[b.actionArgument] = event.eventArgs[b.eventArgument]
         except KeyError, e:
            logging.error("Argument malformed (most likely a typo in config file) : %s" %(e))
      args['user'] = event.recipient

   def getActionsForUser(self, u, event):
      '''
      Search for Actions correponding to event in user u's profile
      '''
      actions = list()
      ep = u.getProfileByEvent(event)
      if (ep != None):
         logging.debug("(eventEngine) user's %s profile for event %s has actions : " %(u.name, event.name))
         for action in ep.getActions():
            newArgs = copy.copy(event.eventArgs) #copy args from event before modifying them
            self.updateArgs(newArgs, ep.getBindingsForAction(action), event)
            actions.append([action, newArgs])
      else:
         logging.error("BEWARE! user %s has no EventProfile attached!!" %(u.name))
      return actions

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
         if (nextEvent.recipient == 'everyone'):
            #get Actions from all Users who actually handle this Event
            for u in userModule.getUsers():
               actionsToExec.extend(self.getActionsForUser(u, nextEvent))
               logging.warning("eventEngine sees user %s" %(u.name)) #TODO: put back on level info/debug
         else:
            u = userModule.getUserByName(nextEvent.recipient)
            if (u != None):
               #get Actions from the specified User
               actionsToExec.extend(self.getActionsForUser(u, nextEvent))
               logging.warning("eventEngine sees Event dedicated to user %s" %(u.name)) #TODO: put back on level info/debug
            else:
               logging.error("Recipient not found for Event %s (recipient: %s)" %(nextEvent.name, nextEvent.recipient) )
         
         if (len(actionsToExec) <= 0):
            logging.warning("no action to execute for event %s, ignoring it" %(nextEvent.name))
         
         for a,args in actionsToExec:
            a(args)
            a.treated = True
      
      time.sleep(5) #TODO: remove ugly sleep and actually wait on synced plugins (eg. voice) to end processing, when needed
      logging.warning("STOPPING")


# To be able to instantiate a sole EventEngine we need to do some dirty tricks:
# Singleton methodology...
class TheEventEngine(EventEngine):

   __instance = EventEngine()

   def __init__(self):
      self.__dict__ = TheEventEngine.__instance.__dict__
      self.__class__ = TheEventEngine.__instance.__class__

