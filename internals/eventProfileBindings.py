import logging
import inspect
import copy
import json

class EventProfileBinding:
   '''
   Represents a binding between an Event and an Action
   one needs to specify the name of the parameters involved in the binding in eventArgument and actionArgument
   '''
   def __init__(self,event,eventArgument, action, actionArgument):
      '''
      Constructor
      Used to bind eventArgument to actionArgument
      '''
      self.event = event
      self.eventArgument = eventArgument
      self.actionArgument = actionArgument
      self.action = action

   def __str__(self):
      return "event %s (%s) to action %s (%s)" % (self.event.name, self.eventArgument, self.action.name, self.actionArgument)

   def dumpJSON(self):
      '''
      Returns a serializable form of the Binding
      This will be dumped as JSON for the WebUI
      '''
      return { 'event':self.event.name, 'action':self.action.name, 'eventArgument':self.eventArgument, "actionArgument":self.actionArgument }

   #this is only for debug purposes, to print out things
   def logBinding(self):
      logging.debug('%s from Event %s binded to %s from Action %s' %(self.eventArgument, self.event.name, self.actionArgument, self.action))
