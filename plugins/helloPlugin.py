import logging
import time
import plugin_def
import action_def

class HelloEvent(action_def.Event):
   def __init__(self):
      super(HelloEvent,self).__init__("HelloEventType", "HelloEvent")
      self.addParameter("helloMsg") #declare exported variables
      self.eventArgs = {'helloMsg' : "Hello, World!"} #instanciate them


class HelloAction(action_def.Action):
   def __init__(self, HelloPlugin):
      super(HelloAction,self).__init__("HelloAction", "HelloAction", HelloPlugin)
      self.addParameter("world") #we expect to receive an argument named 'world'
      self.addParameter("arg2") #we expect to receive an argument named 'arg2'

   def __call__(self, args={}):
      logging.warning("Hello from HelloAction! %s", args)


class helloPlugin(plugin_def.Plugin):
   def __init__(self):
      super(helloPlugin,self).__init__()
      self.addAction(HelloAction(self))
      self.addEvent(HelloEvent())
      self.done = False
   def run(self):
      while (not self.done):
         time.sleep(3)
         self.post(HelloEvent())
   def stop(self):
      self.done = True

