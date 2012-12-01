'''
A Config parser class
'''

from os import path
import logging
import userModule
import eventProfile
import eventProfileBindings
import plugin_mgr
import re

class Config:
   '''
   The Config class is responsible for managing all configuration information related to the testbed site

   '''

   def __init__(self, pathToConfig="metis.conf"):
      '''
      Constructor

      @param path_to_config: path to the testbed overall configuration
      @type path_to_config: string 
      '''

      self.users = {}
      self.currentUser = ""
      self.currentProfile = ""
      self.path = ""

      if path.isfile(pathToConfig):

         # Good, the file exists
         self.path = pathToConfig

         # Now lets try to load it
         if self.__loadConf() == 0:
            raise Exception("config_unreadable")

      else:
         raise Exception("no_config")


   def getUser(self, userName):
      '''
      Returns a User
      '''
      return self.users[userName]

   def saveConf(self):
      '''
      TODO: save the running config into the config file on demand
      '''
      pass

   def __loadConf(self):
      # Private method to load a configuration file at startup
      #   this is where the intelligence of Config is!!

      # Open the configuration file
      conf = open(self.path, 'r')

      if conf:
         # We can open teh configuration file, good

         # Parse the configuration file
         for line in conf.readlines():

            # Clean up the line
            line = line.strip(' \t')
            line = line.rstrip(' \t\n')

            if line:
               # Check if it is a comment
               if line.startswith("#"):
                  continue

               # Check if it is a user definition
               if line.startswith("User"):
                  _,userName = line.split(' ', 1)
                  u = userModule.createNewUser(userName)
                  self.users[userName] = u
                  self.currentUser = u
                  continue

               # Check if it is a EventProfile definition
               if line.endswith(":"):
                  val,_ = line.split(':', 1)
                  eventName = val
                  e = plugin_mgr.ThePluginManager().getEventByName(eventName)
                  if e == None:
                     raise Exception(eventName)
                  p = eventProfile.EventProfile(e)
                  self.currentUser.addEventProfile(p)
                  self.currentProfile = p
                  continue

               # Check if it is a Binding definition
               if line.startswith("Bind"):
                  line = line.replace('Bind ','')  #remove Bind
                  line = line.replace(' ','')      #remove whitespaces
                  line = line.replace('\t','')     #remove tabs
                  #now we can split safely with ':' and '>' to get what we need
                  actionName,eventArgument,actionArgument = re.split('>|:', line)
                  if self.currentProfile != None:
                     a = plugin_mgr.ThePluginManager().getActionByName(actionName)
                     #TODO: check that actionArgument and eventArgument are in action.expectedArgs and event.parameterNames
                     b = eventProfileBindings.EventProfileBinding(self.currentProfile.event, eventArgument, a, actionArgument)
                     self.currentProfile.addBinding(b)
                  continue

               else: 
                  continue

         return 1

      else:
         # Configuration file is unreadable
         return 0
