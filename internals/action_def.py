#!/usr/bin/python

import logging
import inspect
import copy

class Action(object):
   def __init__(self, type = "dummy", name = "dummy", plugin = None):
         self.type = type
         self.name = name
         self.plugin = plugin
         self.grouped = True  #
         self.hiddenFromUI = False

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
   def __init__(self, type=None, name="Null"):
         self.type = type
         self.name = name
         self.treated = 0
         self.actionArgs = {}
         self.hiddenFromUI = False

