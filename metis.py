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
   ThePluginManager().registerPlugin(builtins)
   #epm = EventProfileManager()
   #ThePluginManager().registerPlugin(epm) #here's the good way to register an internal plugin

   #DEBUG STUFF
   '''
   epu = profilesUpdated()

   ep = user.getProfileByEvent(epu)
   if (ep != None):
      
      logging.debug("(eventEngine) user's %s profile for event %s has actions : " %(user.name, epu.name))
      
      for a in ep.getActions():
         logging.debug(a.name)
   else:
      logging.error("BEWARE! user %s has no EventProfile attached!!" %(user.name))

   epu.actionArgs['userName'] = 'Default'
   engine.post(epu)
   '''

   #bind to test EventProfileManager logic
   # NOTE : we need a system to get default bindings (at least for builtin plugins)
   #prof = EventProfile(profilesUpdated())
   #prof.addAction( ThePluginManager().getActionByName("updateProfilesAction") )
   #user.addEventProfile(prof)

   ### Plugin auto-loading stuff
   #basically loads and register the plugins of all python files (*.py) in the "plugins" dir
   #rule is fileName == pluginClassName   
   ###
   for p in glob.glob('plugins/*.py'):
      
      fileName = os.path.basename(p)
      pluginName = string.split(fileName,".")[0]
      logging.warning("Potential plugin %s is available", pluginName)
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
            ThePluginManager().registerPlugin(newplugin)


   ######
   # create Users
   ######
   # TODO: replace with actual user config, most likely read from file
   #createNewUser('Test2')
   #createNewUser('Test')
   #user = createNewUser("Default")
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

   #grants read & write permissions to all, since webserver should have read/write access as well as us
   os.chmod("internals/www/Globals.json", stat.S_IWRITE | stat.S_IREAD | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

   #TODO: set correct permissions on Globals.json so that Webserver can write it too

   ######
   # Generic start
   ######
   engine.start();
   engine.join();
   logging.info("exiting")


# GOTO Main
if __name__ == "__main__":
   main()

