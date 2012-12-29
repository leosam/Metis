import threading
import logging
import os
from plugin_def import *
from action_def import *
from subprocess import *
try:
   import pyttsx
except:
   pass

PLUGIN_NAME = 'festival'
PLUGIN_PREFS = ['volume', 'mark_as_read', 'email', 'token', 'secret']

class festivalEventSay(Event):
   def __init__(self):
      super(festivalEventSay,self).__init__("festivalEventType", "festivalEventSay")


class sayAction(Action):
   def __init__(self, plugin):
      super(sayAction,self).__init__("festivalActionType", "sayAction", plugin)
      self.addParameter("spokenText") #we expect to receive an argument named 'spokenText'

   def __call__(self, args={}):
      try :
         logging.warning("in sayAction : text is %s", args['text']);
      except KeyError:
         args['text'] = "Hello, I'm the new assistant"
      logging.warning("in sayAction : %s", args);
      self.plugin.syncSay(args['spokenText'])


class festivalPlugin(Plugin):
   def __init__(self):
      super(festivalPlugin,self).__init__(PLUGIN_NAME);
      self.addAction(sayAction(self))
      self.addEvent(festivalEventSay())
      self.useFestival = True
      if (not self.useFestival):
         self.engine = pyttsx.init()
         logging.warning("pyttsx initialized");
      else:
         logging.warning("FestivalPlugin initialized");

   def run(self):
      if (not self.useFestival):
         logging.warning("starting pyttsx loop");
         self.engine.startLoop()
         logging.warning("pyttsx loop started ");
      else:
         logging.warning("FestivalPlugin started");

   def stop(self):
      if (not self.useFestival):
         logging.warning("stopping pyttsx loop ");
         self.engine.endLoop()
         logging.warning("pyttsx loop stopped");
      else:
         logging.warning("FestivalPlugin stopped");

   # the main function is here, for saying things
   def say(self, text):
      logging.info("Saying:"+text)
      text=text.encode("latin-1")
      if (self.useFestival):
         """
         this is how we set preferences in festival (only session-wide)
         (Parameter.set 'Audio_Command "aplay -q -c 1 -t raw -f s16 -r $SR $FILE")
         """
         p1 = Popen(["echo", text], stdout=PIPE )
         self.pid = Popen(["festival", "--tts"], stdin=p1.stdout)
      else:
         self.engine.say(text)

   #here's a function that only returns when whole text has been spoken
   def syncSay(self,text):
      self.say(text)
