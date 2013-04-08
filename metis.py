#!/usr/bin/python 

# 
# Metis main code
#
# v0.1 - 2012
#

import sys
sys.path.append('internals')
sys.path.append('plugins')

import threading
import os
import stat
import time
import logging
import inspect
import glob
import importlib
import string
import imp
import json
import config

#ACTIVATE DEBUG LEVEL LOGGING
"""
logging.getLogger().setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
"""

#from globalsManagers import *
from action_def import *
from plugin_def import *
from plugin_mgr import *
from userModule import *
from builtins import *
from eventEngine import *
from eventProfileManager import *

##### MAIN ####

def main():
   
   ######
   # init
   ######

   # Create the singleton EventEngine
   engine = TheEventEngine()

   # First thing to do, before creating users is to correctly bind events & actions to the user's profile
   #registerInternalPlugins()
   builtins = builtinPlugin()
   builtins.module = imp.load_source("builtins","internals/builtins.py")
   ThePluginManager().registerPlugin(builtins) #here's the good way to register a plugin

   #bind to test EventProfileManager logic
   # NOTE : we need a system to get default bindings (at least for builtin plugins)
   #prof = EventProfile(profilesUpdated())
   #prof.addAction( ThePluginManager().getActionByName("updateProfilesAction") )
   #user.addEventProfile(prof)

   ### Plugin auto-loading stuff
   #basically loads and register the plugins of all python files (*.py) in the "plugins" dir
   #instanciate and register all class that are subclass of Plugin
   ###
   for p in glob.glob('plugins/*.py'):
      
      fileName = os.path.basename(p)
      pluginName = string.split(fileName,".")[0]
      logging.info("Potential plugin %s is available", pluginName)
      module = imp.load_source(pluginName,p)
      moduleClasses = inspect.getmembers(module, inspect.isclass)
      pluginClassName = pluginName
      for c in moduleClasses:
         try :
            newObj = c[1]()
            if (issubclass(c[1], Plugin)): #check if potential class is a subclass of Plugin
               newplugin = newObj
               newplugin.module = module
               logging.warning("registering new plugin %s",c[0])
               ThePluginManager().registerPlugin(newplugin)
            else:
               logging.debug("%s is not a Plugin subclass",c[0])
               newObj = None  #discard useless object
         except TypeError as e:
            logging.debug("%s cannot be instanciated as a Plugin %s" %(c[0], e))
            pass


   ######
   # create Users
   ######
   parser = config.Config("internals/metis.conf")


   ######
   # for debug & test purposes
   ######

   #Post a simple event 
   #engine.post(HelloEvent()) 

   #Bind newMailEvent with sayAction 
   #sayaction = ThePluginManager().getActionByName("sayAction")
   #user.getProfileByEvent(newMailEvent()).addAction(sayaction)

   #Test default festival saying
   #engine.post(festivalEventSay()) 



   ######
   # EventProfiles management
   # FIXME: this should be updated whenever a new user is created/deleted, or a plugin is added/removed
   # get all available Actions&Events into json file
   # so our web interface can get them
   ######
   userNames = list()
   for e in getUsers():
      userNames.append( {'name':e.name} )

   actions = ThePluginManager().getAvailableActions()
   actionNames = list()
   for a in actions:
      if (not a.hiddenFromUI):
         actionNames.append( {'name':a.name, 'type':a.type, 'expectedArgs': a.expectedArgs })

   events = ThePluginManager().getAvailableEvents()
   eventNames = list()
   for e in events:
      if (not e.hiddenFromUI):
         eventNames.append( {'name':e.name, 'type':e.type, 'parameterNames': e.parameterNames} )
   f = open("internals/www/Globals.json", 'w')
   try:
      f.write(json.dumps( {'actionsAvailable':actionNames, 'eventsAvailable':eventNames, 'users':userNames} ))
   
      #For debug when 'JSON not serializable object' error: 
      """
      print (actionNames)
      f.write(json.dumps( {'actionsAvailable':actionNames} ))
      f.write(json.dumps( {'eventsAvailable':eventNames} ))
      f.write(json.dumps( {'users':userNames} ))
      """
   except Execption as error_code:
      logging.warning('Error with the json dump')
      quit()
   finally:
      f.close()

   #grant read & write permissions to all, since webserver should have read/write access as well as us
   os.chmod("internals/www/Globals.json", stat.S_IWRITE | stat.S_IREAD | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)


   for u in getUsers():
      u.dumpProfilesJSON()

   ######
   # Generic start
   ######
   ThePluginManager().startPlugins()
   engine.start();
   engine.join();
   logging.info("exiting")


# GOTO Main
if __name__ == "__main__":
   main()

