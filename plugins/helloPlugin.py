import logging
import time
import plugin_def
import action_def

class HelloEvent(action_def.Event):
   def __init__(self):
      super(HelloEvent,self).__init__("HelloEventType", "HelloEvent")


class HelloAction(action_def.Action):
   def __init__(self, HelloPlugin):
      super(HelloAction,self).__init__("HelloAction", "HelloAction1", HelloPlugin)
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
         time.sleep(30)
         self.post(HelloEvent())
   def stop(self):
      self.done = True

