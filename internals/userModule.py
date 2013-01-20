#!/usr/bin/python
import logging
import inspect
import copy
import pluginProfile
import action_def
import json
import os
import stat
from eventProfile import *

#TODO: arguments names bindings in EventProfile

users = list()
def getUsers():
   return users

def getUserByName(name):
   for u in getUsers():
      if (u.name == name):
         return u
   return None

class User:
   def __init__(self,name):
      self.name = name
      self.status = "present"
      self.evtProfs = list()
      self.pluginProfiles = dict()
   """
   Plugin-Profile stuff
   """
   def addPluginProfile(self, plugin, prof):
      try:
         self.pluginProfiles[plugin.name] = prof
      except KeyError:
         #TODO
         logging.error("ERROR: PluginProfile merging not implemented yet!")
   def getPluginProfile(self, plugin):
      try:
         return self.pluginProfiles[plugin.name]
      except KeyError:
         return None

   """
   Event-Profile stuff
   """
   def getProfileByEvent(self,event):
      for p in self.evtProfs:
         if (p.event.name == event.name):
            logging.debug("Found profile for event %s" %(event.name))
            return p
      logging.debug("Warning: Found NO profile for event %s (better create one soon)" %(event.name))
      return None
   def addEventProfile(self,evtprof):
      self.evtProfs.append(evtprof)
   '''
   Write the user's Eventprofiles into a JSON file
   For access via the WebUI
   '''
   def dumpProfilesJSON(self):
      filename = "internals/www/"+self.name+".json"
      f = open(filename, 'w')
      try:
         profs = []
         for p in self.evtProfs:
            profs.append(p.dumpJSON())
         f.write( json.dumps(profs) )
      except Exception as error_code:
         logging.error("Error with the User's json dump : %s" %(error_code))
      finally:
         f.close()
      #now grant read/write permissions to all, since webserver should have read/write access as well as us
      os.chmod(filename, stat.S_IWRITE | stat.S_IREAD | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

   #this is only for debug purposes, to print out things
   def logProfiles(self):
      logging.debug('User %s has:' %(self.name))
      if (len(self.evtProfs) == 0):
         logging.debug('\t\tNO EVENTPROFILES')
      else:
         logging.debug('the following profiles :')
      for ep in self.evtProfs:
         ep.logProfile()
   #TODO: stuff to manage EventProfiles online, per user


#from internalBindings import __bindInternals__
def createNewUser(name, bindInternals=True):
   if (getUserByName(name) != None):
      raise ValueError("user %s already exists" %(name))
   else:
      u = User(name)
      users.append(u) #FIXME possible race between threads
 #     if (bindInternals):
 #        __bindInternals__(u)
      return u

