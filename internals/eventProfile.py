#!/usr/bin/python
import logging
import inspect
import copy
import eventProfileBindings

class EventProfile:
   def __init__(self,event):
      #FIXME: check that event is an actual Event(), not just anything else
      self.event = event
      self.bindings = list()
      self.actions = list()
   def getActions(self):
      return self.actions
   def getBindings(self):
      return self.bindings
   def getBindingsForAction(self, action):
      ba = list()
      for b in self.bindings:
         if (b.action.name == action.name):
            ba.append(b)
      return ba

   def __addAction(self, action):
      self.actions.append(action)

   def addBinding(self, binding):
      try:
         self.bindings.append(binding)
         self.__addAction(binding.action)
      except NameError ,e:
         logging.error("Error trying to add binding to eventProfile %s : %s" %(self.event.name, e) )

   #this is only for debug purposes, to print out things
   def logProfile(self):
      logging.debug('eventProfile for event %s has' %(self.event.name))
      if (len(self.bindings) == 0):
         logging.debug('\t\tNO bindingS')
      else:
         logging.debug('the following bindings :')
      for a in self.bindings:
         a.logBinding
         log.debug('\t')
