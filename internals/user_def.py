#!/usr/bin/python
import logging
import inspect
import copy
import action_def

#TODO: arguments names bindings in EventProfile

class EventProfile:
	def __init__(self,event,actions):
		self.event = event
		self.actions = actions
	def getActions(self):
		return self.actions
	def addAction(self, action):
		self.actions.append(action)


users = list()
def getUsers():
	return users

def createNewUser(name):
   u = User(name)
   users.append(u)
   return u

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
		users.append(self)
	def getProfileByEvent(self,event):
		for p in self.evtProfs:
			if (p.event.name == event.name):
				logging.debug("Found profile for event ",event.name,"\n")
				return p
		logging.debug("ERROR : Found NO profile for event ",event.name,"\n")
		return None
	def addEventProfile(self,evtprof):
		self.evtProfs.append(evtprof)
   #TODO: stuff to manage EventProfiles online, per user


