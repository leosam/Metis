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


   def __witeHeader__(self,conf):
      conf.write("# WARNING: This file has been generated automatically.\n")
      conf.write("# BE CAREFUL to get the syntax right if you choose to edit it\n")
      conf.write("# It works as follows :\n\n")
      conf.write("# Lines beginning with '#' are ignored (comments)\n")
      conf.write("# ### You can define a new user with 'User' command:\n")
      conf.write("# User Default\n")
      conf.write("# ### Inside a user definition, define a Profile for an Event with operator ':'\n")
      conf.write("# \tHelloEvent:\n")
      conf.write("# ### Then, inside a Profile, use the 'Bind' command to bind a parameter from the Event to a parameter from the Action\n")
      conf.write("# \t\tBind HelloAction : helloMsg > ignored\n")
      conf.write("# #\t\tBind sayAction : helloMsg > spokenText\n")
      conf.write("# ### here we specify that upon a newMailEvent, we want 3 fields to be spoken out loud : subject, from and the mail body\n")
      conf.write("# \tnewMailEvent:\n")
      conf.write("# \t\tBind sayAction : subject > spokenText\n")
      conf.write("# \t\tBind sayAction : from > spokenText\n")
      conf.write("# \t\tBind sayAction : body > spokenText\n")
      conf.write("\n")


   def saveConf(self):
      '''
      save the running config into the config file on demand
      '''
      conf = open(self.path, 'w')
      if conf:
         # We can open the configuration file, good
         self.__witeHeader__(conf)

         for u in userModule.getUsers():
            conf.write("User %s" %(u.name))
            for p in u.evtProfs:
               conf.write("\t%s:" %(p.event.name))
               for b in p.getBindings():
                  conf.write("\t\tBind %s : %s > %s" %(b.action.name, b.eventArgument, b.actionArgument) )
            conf.write("\n")
         conf.write("\n")
      else :
         logging.error("Cannot open config file %s to save config!" % (self.path))

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

         logging.info("Configuration file %s successfuly read" %(self.path))
         return 1

      else:
         logging.error("Configuration file %s is unreadable!" %(self.path))
         return 0
