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


class newUser(builtinEvent):
   def __init__(self):
      super(builtinEvent,self).__init__(type="EventProfileEvent", name="newUser");

class profilesUpdated(builtinEvent):
   def __init__(self):
      super(builtinEvent,self).__init__(type="EventProfileEvent", name="profilesUpdated");

# private function that actually does the work
def __updateProfiles__(user, profiles):
   logging.warning("updating profile for %s" %(user.name))
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
      except e:
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
      except e:
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

   def loadProfilesFromFile(self, path, manager):
      logging.warning("whoohoo 1" )
      fd = os.path.basename(path)
      logging.warning("whoohoo 2" )
      (name,ext) = os.path.splitext(fd)
      logging.warning("whoohoo 3 %s" %(manager.profiles) )
      if (name == "Globals"):
         raise ValueError("this file doesn't contain eventProfile") #it's system-wide while we expect user-specific
      if (not name in manager.profiles):
         manager.profiles[name] = internalProfile()
      p = manager.profiles[name]
      logging.warning("opening %s" %(path))
      f = open(path,'r')
      try:
         logging.warning("reading from %s" %(path))
         lines = f.read()
         logging.warning("JSON from read")
         p.data = json.loads(lines)
         logging.warning("JSON ready")
      except Exception, e:
         logging.error("Error : %s" %(e))
      finally:
         f.close()
         logging.warning("file closed p=%s" %(p))
      p.profiles = list()
      for event in p.data:
         logging.warning("in for 1")
         actions = list();
         logging.warning("in for 1.5")
         for a in p.data[0]['actions']:
            logging.warning("in for 2")
            if (not a['removed']):
               name = manager.manager.getActionByName(a['name']) #TODO: TOFIX: a['name'] doesn't necessarily exists
               actions.append( name )
         e = manager.manager.getEventByName(p.data['name'])
         logging.warning("in for 3")
         p.profiles.append(EventProfile(e, actions))
         logging.warning("in for 4")
      manager.profiles[name].profiles = p.profiles
      logging.warning("loadProfilesFromFile DONE")
   
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
      path = obsEvent.src_path
      self.loadProfilesFromFile(path, self.eventProfileManager)
      event = profileUpdated()
      event.actionArgs = {'userName':f, 'profiles':self.eventProfileManager.profiles[f].profiles}
      self.eventProfileManager.post(event)
   def on_modified(self, obsEvent):
      logging.warning ("seen %s" %(obsEvent) )
      path = obsEvent.src_path
      logging.warning (" loadProfilesFromFile (%s, %s) " %(path, self.eventProfileManager))
      try:
         self.loadProfilesFromFile(path, self.eventProfileManager)
         logging.warning ("DONE!!" )
         event = profileUpdated()
         event.actionArgs = {'userName':f, 'profiles':self.eventProfileManager.profiles[f].profiles}
         logging.warning ("will post event %s" %(event.name) )
         self.eventProfileManager.post(event)
         logging.warning ("POSTED %s" %(event.name) )
      except Exception,e:
         logging.error("Exception : %s" %(e))


