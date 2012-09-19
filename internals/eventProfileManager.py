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
      super(builtinEvent,self).__init__();

class profilesUpdated(builtinEvent):
   def __init__(self):
      super(builtinEvent,self).__init__();

# private function that actually does the work
def __updateProfiles__(user, profiles):
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
      super(builtinAction,self).__init__(plugin=eventProfilePlugin);
      self.name = "handleNewUserAction"
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
      super(builtinAction,self).__init__(plugin=eventProfilePlugin);
      self.name = "updateProfilesAction"
   def __call__(self,args={}):
      try:
         name = args['userName']
         profiles = args['profiles']
      except e:
         logging.error("action called with wrong parameters : %s" %(e))
         return
      u = getUserByName(name)
      __updateProfiles__(u, profiles)


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
      fd = os.path.basename(path)
      (name,ext) = os.path.splitext(fd)
      p = manager.profiles[name]
      f = open(path,'w')
      try:
         p.data = json.loads(f.read())
      except e:
         logging.error("Error : %s" %(e))
      finally:
         f.close()
      p.profiles = list()
      for event in p.data:
         actions = list();
         for a in p.data['actions']:
            if (not a.removed):
               actions.append( self.manager.getActionByName(a.name) )
         e = self.manager.getEventByName(p.data['name'])
         p.profiles.append(EventProfile(e, actions))
      manager.profiles[name].profiles = p.profiles

   def run(self):
      self.handler = ActivityHandler(self)
      self.observer = Observer()
      self.observer.schedule(self.handler, path="internals", recursive=False)
      logging.warning("EventProfileManager : observer starts")
      self.observer.start()
      """
      while (not self.finished):
         for path in os.listdir(os.path.join(os.getcwd(), "internals")):
            fd = os.path.basename(path)
            (f,ext) = os.path.splitext(fd)
            if (ext == ".json" and f != "Globals"):
               fstats = os.stat(path)
               try:
                  if (self.profiles[f].st_mtime < fstats.st_mtime):
                     self.loadProfilesFromFile(path)
                     event = profileUpdated()
                     event.actionArgs = {'userName':f, 'profiles':self.profiles[f].profiles}
               except:
                  self.profiles[f].st_mtime = fstats.st_mtime
                  self.loadProfilesFromFile(path)
                  event.newUser()
                  event.actionArgs = {'userName':f, 'profiles':self.profiles[f].profiles}
               finally:
                  self.post(event)
         time.sleep(self.interval)
         """
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
      self.loadProfilesFromFile(path, self.eventProfileManager)
      event = profileUpdated()
      event.actionArgs = {'userName':f, 'profiles':self.eventProfileManager.profiles[f].profiles}
      self.eventProfileManager.post(event)


