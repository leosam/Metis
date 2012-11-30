#!/usr/bin/python

import logging
import inspect
import copy
import sys
import time
import json
import os
import os.path

from watchdog.observers import Observer
import watchdog

from builtins import *
from plugin_def import *
from action_def import *
from userModule import *

class newUser(builtinEvent):
   def __init__(self):
      super(builtinEvent,self).__init__(type="EventProfileEvent", name="newUserEvent")
      self.hiddenFromUI = True

class profilesUpdated(builtinEvent):
   def __init__(self):
      super(builtinEvent,self).__init__(type="EventProfileEvent", name="profilesUpdatedEvent")
      self.hiddenFromUI = True

from internalBindings import __bindInternals__

# private function that actually does the work
def __updateProfiles__(user, profiles):
   if (user != None):
      logging.warning("updating profile for %s" %(user.name))
      user.evtProfs = list() #clear all existing profiles
      for p in profiles:
         logging.info("new profile for %s contains actions for %s" %(user.name, p.event.name))
         user.addEventProfile(p)
      #always bind ourselves, otherwise it only works once and we can't modify the profile anymore
      __bindInternals__(user)


############
# IMPORTANT NOTE: 
#  we define builtin Actions here to prevent
#  any race condition when accessing EventProfiles
#  ie. the eventManager is alone processing those profiles
#  the eventProfileManager does not modify them directly
###########

class handleNewUser(builtinAction):
   def __init__(self, eventProfilePlugin):
      super(builtinAction,self).__init__(name="handleNewUserAction", type="EventProfileAction",plugin=eventProfilePlugin);
      self.hiddenFromUI = True
   def __call__(self,args={}):
      try:
         name = args['userName']
      except Exception, e:
         logging.error("action called with wrong parameters : expected %s but got %s" %(e,str(args)))
         return
      u = createNewUser(name)
      __bindInternals__(u)

class updateProfiles(builtinAction):
   def __init__(self, eventProfilePlugin):
      super(builtinAction,self).__init__(name="updateProfilesAction", type="EventProfileAction",plugin=eventProfilePlugin);
      self.hiddenFromUI = True
   def __call__(self,args={}):
      try:
         name = args['userName']
         profiles = args['profiles']
      except Exception, e:
         logging.error("action called with wrong parameters : expected %s but got %s" %(e,str(args)))
         return
      u = getUserByName(name)
      __updateProfiles__(u, profiles)


#internal representation of EventProfiles from json files
class internalProfile():
   data = None
   profiles = list()
   pass

class EventProfileManager(builtinPlugin):
   def __init__(self):
      super(EventProfileManager,self).__init__();
      self.addAction(handleNewUser(self))
      self.addAction(updateProfiles(self))
      self.addEvent(newUser())
      self.addEvent(profilesUpdated())
      self.handler = ActivityHandler(self)
      self.finished = False
      self.profiles = {} #keep the profiles seen so we won't trigger 2 events for the same modification
      self.interval = 2  #time interval between 2 checks #VALUE IS FOR DEBUG

   def getUserFromPath(self, path):
      fd = os.path.basename(path)
      (name,ext) = os.path.splitext(fd)
      return name

   def loadUsersFromGlobals(self, path, manager):
      name = self.getUserFromPath(path)
      if (name != "Globals"):
         raise ValueError("file '%s' doesn't contain globals variables" %(path)) #it's user-specific while we expect system-wide
      logging.info("opening %s" %(path))
      f = open(path,'r')
      try:
         logging.info("reading from %s" %(path))
         lines = f.read()
         logging.info("JSON from read")
         rawdata = json.loads(lines)
         data = rawdata
      except Exception, e:
         logging.error("Error : %s" %(e))
      finally:
         f.close()
         logging.info("file Globals.json closed")
      manager.users = list()
      for u in data['users']:
         logging.debug("found user %s" %(u) )
         manager.users.append(u)

   def loadProfilesFromFile(self, path, manager):
      name = self.getUserFromPath(path)
      if (name == "Globals"):
         raise ValueError("file '%s' doesn't contain eventProfile" %(path)) #it's system-wide while we expect user-specific
      if (not name in manager.profiles):
         manager.profiles[name] = internalProfile()
      p = manager.profiles[name]
      logging.info("opening %s" %(path))
      f = open(path,'r')
      try:
         logging.info("reading from %s" %(path))
         lines = f.read()
         logging.info("JSON from read")
         rawdata = json.loads(lines)
         p.data = rawdata
      except Exception, e:
         logging.error("Error : %s" %(e))
      finally:
         f.close()
         logging.info("file closed p=%s" %(p))
      p.profiles = list()
      for eventIdx in range(len(p.data)):
         event = p.data[eventIdx]
         logging.debug("for event %s" %(event) )
         actions = list()
         for a in event['actions']:
            logging.debug("found action %s " %(a) )
            if (not a['removed']):
               actionHandle = manager.manager.getActionByName(a['name'])
               logging.debug(" got handle %s for action %s " %(actionHandle, a['name'] ))
               actions.append( actionHandle )
         e = manager.manager.getEventByName(event['name'])
         logging.debug("found event %s, adding actions %s" %(e,actions) )
         #FIXME: adapt to Bindings system
         p.profiles.append(EventProfile(e, actions))
      manager.profiles[name].profiles = p.profiles
      logging.info("loadProfilesFromFile DONE")
   
   def post(self, event):
      logging.debug("Posting from EventProfileManager");
      super(EventProfileManager, self).post(event)

   def run(self):
      self.handler = ActivityHandler(self)
      self.observer = Observer()
      self.observer.schedule(self.handler, path="internals/www", recursive=False)
      logging.warning("EventProfileManager : observer starts")
      self.observer.start()
      self.observer.join()
      logging.warning("EventProfileManager stops")

   def stop(self):
      logging.warning("EventProfileManager asked to stop")
      self.observer.stop()

class ActivityHandler(watchdog.events.FileSystemEventHandler,EventProfileManager):
   def __init__(self,evtProfMgr):
      self.eventProfileManager = evtProfMgr
   def on_created(self, obsEvent):
      logging.warning ("seen created file %s" %(obsEvent) )
      #do nothing with for now
      #TODO: create new user and add default EventProfile
   def on_modified(self, obsEvent):
      logging.warning ("seen modified file %s" %(obsEvent) )
      path = obsEvent.src_path
      name = self.getUserFromPath(path)
      if (name != "Globals"): #update eventProfile for the user
         try:
            self.loadProfilesFromFile(path, self.eventProfileManager)
            logging.debug("DONE!!")
         except ValueError,e:
            logging.info("Ignoring %s" %(e))
         except Exception,e:
            logging.error("Error (1) Exception : %s" %(e))
         try:
            event = profilesUpdated()
            name = self.eventProfileManager.getUserFromPath(path)
            event.actionArgs = {'userName':name, 'profiles':self.eventProfileManager.profiles[name].profiles}
            logging.info("(EventProfileManager 1)will post event %s" %(event.name) )
            self.eventProfileManager.post(event)
            logging.debug("POSTED %s" %(event.name) )
         except Exception,e:
            logging.error("Error (2) Exception : %s" %(e))
      else: #update users list
         try:
            logging.debug("TRying to update Globals\n")
            self.loadUsersFromGlobals(path, self.eventProfileManager)
            logging.debug("DONE!!")
         except ValueError,e:
            logging.info("Ignoring %s" %(e))
         except Exception,e:
            logging.error("Error (3) Exception : %s" %(e))
         try:
            for u in self.eventProfileManager.users:
               if (getUserByName(u['name']) == None):
                  event = newUser()
                  event.actionArgs = {'userName':u['name']}
                  logging.info("(EventProfileManager 2) will post event %s for user %s creation" %(event.name, u['name']) )
                  self.eventProfileManager.post(event)
                  logging.debug("POSTED %s" %(event.name) )
         except Exception,e:
            logging.error("Error (4) Exception : %s" %(e))

