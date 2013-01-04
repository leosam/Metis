import logging
import time
import plugin_def
import action_def

"""
Here is the interface of the plugin :
- NAME should be unique (not 2 plugins with the same name during the same execution)
- USER_POLICY specifies wether the plugin should be handled on a 'perUser' basis (email, social network accounts should be perUser), or is 'global' (the default) to all Users (everything related to the house should probably global).
   'perUser' plugins are ensured to have a 'user' attribute before their thread is started
- PREFS represents the plugin's preferences variables. Each user can specify them in their respective config file. Default values should apply if none provided.
"""
PLUGIN_NAME = 'hello'
#PLUGIN_USER_POLICY = 'global'
PLUGIN_USER_POLICY = 'perUser'
PLUGIN_PREFS = ['interval', 'count']


class HelloEvent(action_def.Event):
   def __init__(self):
      super(HelloEvent,self).__init__("HelloEventType", "HelloEvent")
      self.addParameter("helloMsg") #declare exported variables
      self.eventArgs = {'helloMsg' : "Hello, World!"} #instanciate them


class HelloAction(action_def.Action):
   def __init__(self, HelloPlugin):
      super(HelloAction,self).__init__("HelloAction", "HelloAction", HelloPlugin)
      self.addParameter("world") #This Action expect to receive/can use an argument named 'world'
      self.addParameter("arg2") #This Action expect to receive/can use an argument named 'arg2'
      """
      Those parameters will be binded to (have the same value as) variables from the calling Event
      This way Event's variables names can differ from Action's parameters names
      """

   def __call__(self, args={}):
      logging.warning("Hello from HelloAction! %s", args)


class helloPlugin(plugin_def.Plugin):
   def __init__(self):
      """
      Calling super's constructor is needed, to create Metis' Plugin internal structure
      """
      super(helloPlugin,self).__init__(PLUGIN_NAME)
      """
      Then we register all Actions and Events this plugin can trigger
      """
      self.addAction(HelloAction(self))
      self.addEvent(HelloEvent())
      self.done = False
      """
      Set default preferences values
      """
      self.interval = 3
      self.count = 1

   """
   Here's the main code of the plugin
   This is executed inside the plugin's own thread
   """
   def run(self):
      i = 0
      #get count value if user defined it, if not we use default value 
      if (self.getPluginProfile(self.user) ):
         #Beware: Prefs come from config file as string, need appropriate cast (int here)
         try:
            self.count = int(self.getPluginProfile(self.user).getPref("count"))
         except KeyError:
            pass

         # always expect a KeyError on each Pref if the Pref isn't redefined by user in config
         try:
            self.interval = int(self.getPluginProfile(self.user).getPref("interval")) 
         except KeyError:
            pass
      
      #Here's the main code
      while (not self.done):
         time.sleep(self.interval)
         self.post(HelloEvent())
         i = i+1
         if (i == self.count):
            self.stop()
      logging.warning("HelloPlugin ends for %s " %(self.user.name))

   def stop(self):
      self.done = True

