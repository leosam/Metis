import threading
import logging
import os
from plugin_def import *
from action_def import *
from subprocess import *
import fcntl
import time
try:
   import pyttsx
except:
   pass

PLUGIN_NAME = 'festival'
#PLUGIN_USER_POLICY = 'global' #default setting
PLUGIN_PREFS = ['volume', 'mark_as_read', 'email', 'token', 'secret']

class festivalEventSay(Event):
   def __init__(self):
      super(festivalEventSay,self).__init__("festivalEventType", "festivalEventSay")
      self.addParameter("toSay") #declare exported variables


class sayAction(Action):
   def __init__(self, plugin):
      super(sayAction,self).__init__("festivalActionType", "sayAction", plugin)
      self.addParameter("spokenText") #we expect to receive an argument named 'spokenText'

   def __call__(self, args={}):
      try :
         logging.warning("in sayAction : text is %s", args['spokenText']);
      except KeyError:
         args['spokenText'] = "Hello, I'm the new assistant"
      logging.warning("in sayAction : %s", args);
      self.plugin.syncSay(args['spokenText'])


class festivalPlugin(Plugin):
   def __init__(self):
      super(festivalPlugin,self).__init__(PLUGIN_NAME);
      self.addAction(sayAction(self))
      self.addEvent(festivalEventSay())
      self.useFestival = True
      self.pipe = None #used for communicating with festival process (festival's stdin)
      self.pipeout = None #used for communicating with festival process (festival's stdout & stderr)
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
         self.popen = Popen(["festival"], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
         self.pipe = self.popen.stdin
         self.pipeout = self.popen.stdout
         #UNIX solution for nonblocking reads...sorry about portability :p
         fcntl.fcntl(self.pipeout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK) 
         logging.warning("FestivalPlugin started");
         self.syncSay("Metis is up and ready") #preload voice in cache, takes a while but speeds up further calls

   def stop(self):
      if (not self.useFestival):
         logging.warning("stopping pyttsx loop ");
         self.engine.endLoop()
         logging.warning("pyttsx loop stopped");
      else:
         self.popen.terminate()
         logging.warning("FestivalPlugin stopped");

   # the main function is here, for saying things
   def say(self, text):
      logging.info("Saying:"+text)
      text=text.encode("latin-1")
      if (self.useFestival):
         text.replace('"', '\"')
         cmd = "(SayText \""+text+"\")\n"
         logging.info("[FESTIVAL] sending cmd: %s" %(cmd))
         cmd += "(help)\n" #we add this to get output from festival after saying so we can have a synchronizedSay function
         self.pipe.write(cmd)
      else:
         self.engine.say(text)

   #here's a function that only returns when whole text has been spoken
   #BEWARE: syncSay works only when everyone uses syncSay
   # there is no synchronization guaranteed when mixed use of say and syncSay
   def syncSay(self,text):
      self.say(text)
      logging.debug("festival after saying, attempting to readline()")
      gotOutput = False
      msg = ""
      #now get output of (help) when it's ready
      while (not gotOutput):
         try :
            time.sleep(0.1)
            msg = self.pipeout.read() 
            gotOutput = True
         except IOError as e:
            time.sleep(0.1)
      logging.debug("festival (help) says: %s" %(msg)) #TODO: downgrade to info

