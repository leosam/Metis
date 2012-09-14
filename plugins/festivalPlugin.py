import threading
import logging
import os
import pyttsx
from plugin_def import *
from action_def import *

class festivalEventSay(Event):
   def __init__(self):
      super(festivalEventSay,self).__init__("festivalEventType", "festivalEventSay")


class sayAction(Action):
   def __init__(self, plugin):
      super(sayAction,self).__init__("festivalActionType", "sayAction", plugin)
   def __call__(self, args={}):
      try :
         logging.warning("in sayAction : text is %s", args['text']);
      except KeyError:
         args['text'] = "Hello, I am the new guy"
      logging.warning("in sayAction : %s", args);
      self.plugin.syncSay(args['text'])


class festivalPlugin(Plugin):
   def __init__(self):
      super(festivalPlugin,self).__init__();
      self.addAction(sayAction(self))
      self.addEvent(festivalEventSay())
      self.engine = pyttsx.init()
      logging.warning("pyttsx initialized");

   def run(self):
      logging.warning("starting pyttsx loop");
      self.engine.startLoop()
      logging.warning("pyttsx loop started ");

   def stop(self):
      logging.warning("stopping pyttsx loop ");
      self.engine.endLoop()
      logging.warning("pyttsx loop stopped");

   # the main function is here, for saying things
   def say(self, text):
      logging.info("Saying:"+text)
      self.engine.say(text)

   def syncSay(self,text):
      self.say(text)
      while (self.engine.isBusy()):
         pass
