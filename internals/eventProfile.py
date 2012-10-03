#!/usr/bin/python
import logging
import inspect
import copy

#TODO: arguments names bindings in EventProfile

class EventProfile:
   def __init__(self,event,actions=None):
      #FIXME: check that event is an actual Event(), not just anything else
      self.event = event
      #Note:we can't create an empty list with default parameters, because then this list would be shared across all profiles, and we don't want that...
      if (actions == None):
         self.actions = list()
      else:
         self.actions = actions
   def getActions(self):
      return self.actions
   def addAction(self, action):
      try:
         self.actions.append(action)
      except NameError ,e:
         logging.error("Error trying to add action to eventProfile %s : %s" %(self.event.name, e) )
   #this is only for debug purposes, to print out things
   def logProfile(self):
      logging.debug('eventProfile for event %s has' %(self.event.name))
      if (len(self.actions) == 0):
         logging.debug('\t\tNO ACTIONS')
      else:
         logging.debug('the following actions :')
      for a in self.actions:
         logging.debug('\t%s' %(a.name))
