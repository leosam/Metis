#!/usr/bin/python
import sys
sys.path.append('internals')
sys.path.append('plugins')

import threading
import os
import time
import logging
import inspect
import glob
import importlib
import string
import imp
import json

from action_def import *
from plugin_mgr import *
from plugin_def import *
from user_def import *
from builtins import *
from eventProfileManager import *
from engine import *
from globalsManagers import *

##### MAIN ####

######
#init
######
engine.getPluginManager().registerPlugin(builtins) #don't start useless thread
#epm = EventProfileManager()
#print dir(epm)

#engine.getPluginManager().registerPlugin(epm) #here's the good way to register an internal plugin


# TODO: replace with actual user config, most likely read from file
User("Test2")
user = User("Test")

### Plugin auto-loading stuff
#basically loads and register the plugins of all python files (*.py) in the "plugins" dir
#rule is fileName == pluginClassName
###
for p in glob.glob('plugins/*.py'):
   fileName = os.path.basename(p)
   pluginName = string.split(fileName,".")[0]
   logging.warning("Plugin %s is available", pluginName)
   module = imp.load_source(pluginName,p)
   #module = importlib.import_module(pluginName) #alternate import method, same thing
   #classes = inspect.getmembers(sys.modules[pluginName], inspect.isclass)
   moduleClasses = inspect.getmembers(module, inspect.isclass)
   pluginClassName = pluginName
   for c in moduleClasses:
      globals()[c[0]] = c[1]  #UGLY HACK : since import does not put the classes into globals, we do it manually...(hopefully that's enough for complex plugins ?)
      if (c[0] == pluginClassName): #find the plugin's main class #TOFIX: try to find Plugin in parents of this class?
         newplugin = c[1]()
         logging.warning("registering new plugin %s",pluginClassName)
         engine.getPluginManager().registerPlugin(newplugin)
######
# for debug & test purposes
######

#Post a simple event
engine.post(HelloEvent()) 

#Bind newMailEvent with sayAction 
#sayaction = engine.getPluginManager().getActionByName("sayAction")
#user.getProfileByEvent(newMailEvent()).addAction(sayaction)

#Test default festival saying
#engine.post(festivalEventSay()) 



######
# EventProfiles management
# get all available Actions&Events into json files
# so our web interface can get them
######
userNames = list()
for e in getUsers():
   userNames.append( {'name':e.name} )

actions = engine.getPluginManager().getAvailableActions()
actionNames = list()
for a in actions:
   actionNames.append( {'name':a.name, 'type':a.type }) #TODO: find a way to handle action 'input' args

events = engine.getPluginManager().getAvailableEvents()
eventNames = list()
for e in events:
   eventNames.append( {'name':e.name, 'type':e.type} ) #TODO: find a way to handle event 'output' args
f = open("internals/Globals.json", 'w')
try:
   f.write(json.dumps( {'actionsAvailable':actionNames, 'eventsAvailable':eventNames, 'users':userNames} ))
finally:
   f.close()

######
# Generic start
######
engine.start();
engine.join();
logging.info("exiting")
