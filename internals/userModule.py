#!/usr/bin/python
import logging
import inspect
import copy
import action_def
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
      self.pluginProf = None
   def getProfileByEvent(self,event):
      for p in self.evtProfs:
         if (p.event.name == event.name):
            logging.debug("Found profile for event %s" %(event.name))
            return p
      logging.debug("Warning: Found NO profile for event %s (better create one soon)" %(event.name))
      return None
   def addEventProfile(self,evtprof):
      self.evtProfs.append(evtprof)
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
      users.append(u)
 #     if (bindInternals):
 #        __bindInternals__(u)
      return u

