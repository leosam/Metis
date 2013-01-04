import logging
import inspect
import copy

class Action(object):
   def __init__(self, type = "dummy", name = "dummy", plugin = None):
      self.type = type
      self.name = name
      self.plugin = plugin
      self.grouped = False  #
      self.hiddenFromUI = False
      self.expectedArgs = list()
   def addParameter(self, name):
      self.expectedArgs.append(name)
   '''
   Returns a serialized representation
   Will be used as JSON in WebUI
   '''
   def dumpJSON(self):
      return {'name':self.name, 'type':self.type, 'hiddenFromUI':self.hiddenFromUI, 'expectedArgs':self.expectedArgs}

   def __call__(self,newargs={}):
      args = copy.copy(self.init_args)
      args.update(newargs)
      try:
         self.type = args['type']
         self.name = args['name']
      except KeyError:
         pass
      try:
         self.plugin = args['plugin']
      except KeyError:
         pass
      logging.debug('calling Action %s(%s) with args : %s' %(self.name, inspect.getmembers(self,inspect.isfunction)[0], args ))

class Event(object):
   def __init__(self, type=None, name="Null", recipient="everyone"):
      self.type = type
      self.name = name
      self.recipient = recipient
      self.treated = 0
      self.eventArgs = {}
      self.hiddenFromUI = False
      self.parameterNames = list()  #exported list of keys used in actionArgs
   def addParameter(self, name):
      self.parameterNames.append(name)

