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

from plugin_def import *
from builtins   import *
from action_def import *
from user_def import *


class newUser(builtinEvent):
   def __init__(self):
      super(builtinEvent,self).__init__(type="EventProfileEvent", name="newUser");

class profilesUpdated(builtinEvent):
   def __init__(self):
      super(builtinEvent,self).__init__(type="EventProfileEvent", name="profilesUpdated");

# private function that actually does the work
def __updateProfiles__(user, profiles):
   logging.warning("updating profile for %s" %(user.name))
   if (len(profiles) > 0):
      user.evtProfs = list() #clear all existing profiles
      for p in profiles:
         user.addEventProfile(p);

############
# IMPORTANT NOTE: 
#  we use Actions here to prevent
#  any race condition when accessing EventProfiles 
#  ie. the eventManager is alone processing those
###########

class handleNewUser(builtinAction):
   def __init__(self, eventProfilePlugin):
      super(builtinAction,self).__init__(name="handleNewUserAction", type="EventProfileAction",plugin=eventProfilePlugin);
   def __call__(self,args={}):
      try:
         name = args['userName']
         profiles = args['profiles']
      except Exception, e:
         logging.error("action called with wrong parameters : %s" %(e))
         return
      u = createNewUser(name)
      __updateProfiles__(u, profiles)

class updateProfiles(builtinAction):
   def __init__(self, eventProfilePlugin):
      super(builtinAction,self).__init__(name="updateProfilesAction", type="EventProfileAction",plugin=eventProfilePlugin);
   def __call__(self,args={}):
      try:
         name = args['userName']
         profiles = args['profiles']
      except Exception, e:
         logging.error("action called with wrong parameters : %s" %(e))
         return
      u = getUserByName(name)
      __updateProfiles__(u, profiles)


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
         logging.warning("for event %s" %(event) )
         actions = list()
         for a in event['actions']:
            logging.warning("found action %s " %(a) )
            if (not a['removed']):
               actionHandle = manager.manager.getActionByName(a['name']) #TODO: TOFIX: a['name'] doesn't necessarily exists
               logging.warning(" got handle %s for action %s " %(actionHandle, a['name'] ))
               actions.append( actionHandle )
         e = manager.manager.getEventByName(event['name'])
         logging.warning("found event %s, adding actions %s" %(e,actions) )
         p.profiles.append(EventProfile(e, actions))
      manager.profiles[name].profiles = p.profiles
      logging.info("loadProfilesFromFile DONE")
   
   def post(self, event):
      logging.warning("Posting from EventProfileManager");
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
      #super(ActivityHandler,self).__init__();
      self.eventProfileManager = evtProfMgr
   def on_created(self, obsEvent):
      logging.warning ("seen created file %s" %(obsEvent) )
      #do nothing with for now
      #TODO: create new user and add default EventProfile
      """
      path = obsEvent.src_path
      try:
         self.loadProfilesFromFile(path, self.eventProfileManager)
         logging.warning ("DONE!!" )
      except ValueError,e:
         logging.error("CATCHED VALUE Exception : %s" %(e))
      except Exception,e:
         logging.error("CATCHED Exception : %s" %(e))
      event = profilesUpdated()
      name = self.eventProfileManager.getUserFromPath(path)
      event.actionArgs = {'userName':name, 'profiles':self.eventProfileManager.profiles[name].profiles}
      self.eventProfileManager.post(event)
      """
   def on_modified(self, obsEvent):
      logging.warning ("seen modified file %s" %(obsEvent) )
      path = obsEvent.src_path
      try:
         self.loadProfilesFromFile(path, self.eventProfileManager)
         logging.warning ("DONE!!" )
      except ValueError,e:
         logging.error("BAD VALUE Exception : %s" %(e))
      except Exception,e:
         logging.error("CATCHED 1 Exception : %s" %(e))
      try:
         event = profilesUpdated()
         name = self.eventProfileManager.getUserFromPath(path)
         event.actionArgs = {'userName':name, 'profiles':self.eventProfileManager.profiles[name].profiles}
         logging.warning ("will post event %s" %(event.name) )
         self.eventProfileManager.post(event)
         logging.warning ("POSTED %s" %(event.name) )
      except Exception,e:
         logging.error("CATCHED 2 Exception : %s" %(e))


