import logging
import time
import socket
import SocketServer
import userModule
import eventProfile
import eventProfileBindings
import plugin_def
import plugin_mgr
import action_def

PLUGIN_NAME = 'shell'
PLUGIN_USER_POLICY = 'global'
PLUGIN_PREFS = []
PLUGIN_HOST = "localhost"  #only listen to localhost by default (don't accept external connections)
#PLUGIN_HOST = "0.0.0.0"    #listen to all interfaces
PLUGIN_PORT = 2222   #as any port, value below 1024 needs root access
PLUGIN_USERNAME = "shell"  #this is the Metis user used to send events to Metis engine


#In case anyone would like to hook themselves, we send an event for every command typed in
class ShellCmdEvent(action_def.Event):
   def __init__(self):
      super(ShellCmdEvent,self).__init__("ShellEventType", "ShellCmdEvent")
      self.addParameter("cmd") #declare exported variables

###### command handlers ######
def shellExit(ignoredArgs):
   return "Byebye"

def displayShellHelp(ignoredArgs):
   response = "welcome to Metis' shell\r\n"
   response += "Here is a list of the available commands:\r\n"
   for c in handlers.items():
      response +="\t%s : %s\r\n" %(c[0], c[1]['help'])
   return response

def say(text):
   response = None
   a = plugin_mgr.ThePluginManager().getActionByName("sayAction")
   u = userModule.getUserByName(PLUGIN_USERNAME)
   if (a):
      #add appropriate eventProfile to our user so that sayAction gets executed when we post festivalEventSay
      event = plugin_mgr.ThePluginManager().getEventByName("festivalEventSay") #the event we will trigger
      if (event == None):
         raise Exception("found sayAction but not festivalEventSay")
      if (u.getProfileByEvent(event) == None):
         profile = eventProfile.EventProfile(event)
         #festivalEventSay has argument 'toSay' and sayAction expects "spokenText", so bind them
         binding = eventProfileBindings.EventProfileBinding(event, "toSay", a, "spokenText") 
         profile.addBinding(binding)

         #add profile to shell user
         u.addEventProfile(profile)

      #send appropriate event
      event.eventArgs = {'toSay' : text} #add text to event
      event.post()
   else:
      response = "Cannot find sayAction to say text, please register festivalPlugin"
   return response

handlers = {
      #Add handlers here syntax is : 
      #Command: {'fun': handler, 'help': helpText}
      "stop": {"fun":shellExit, "help": "terminates the shell session"},
      "quit": {"fun":shellExit, "help": "terminates the shell session"},
      "exit": {"fun":shellExit, "help": "terminates the shell session"},
      "help": {"fun":displayShellHelp, "help": "prints this help"},
      "?": {"fun":displayShellHelp, "help": "prints this help"},
      "say": {"fun":say, "help": "say text out loud "} #depends on FestivalPlugin availability
      }

####### shell  ######
#"request" in BaseRequestHandler actually means connection
class shell(SocketServer.BaseRequestHandler):
   def handle(self):
      self.loop = True
      self.prompt = "shell@Metis$> "
      try:
         while (self.loop):
            #print prompt
            self.request.sendall(self.prompt)
            #get user request
            self.cmd = self.request.recv(1024)
            if (self.cmd == '\x04' or self.cmd == '\4'): #handle EOF
               self.cmd = "exit"
            self.cmd = self.cmd.strip()
            logging.debug("TCP received |%s|" %(self.cmd))
            logging.warning("[Shell] cmd BEFORE %s" %(self.cmd))
            self.cmd.lower()
            self.cmd = self.cmd.replace('"','\\"')
            self.cmd = self.cmd.replace("'","\\'")
            logging.warning("[Shell] cmd AFTER %s" %(self.cmd))
            if (self.cmd != ''):
               #generate event
               e = ShellCmdEvent()
               e.eventArgs = {'cmd' : self.cmd}
               e.post()
               #call appropriate handler
               self.response = self.buildResponse()
               if (self.response != None):
                  #send response
                  self.response += "\r\n"
                  logging.debug("Built response : %s" %(self.response) )
                  self.request.sendall(self.response)
               if (self.cmd == "stop" or self.cmd == "quit" or self.cmd == "exit"):
                  self.loop = False
      except Exception as e:
         logging.error("[Shell] connection error : %s" %(e))
      finally:
         #clean TCP connection
         try:
            self.request.shutdown(socket.SHUT_RDWR)
         except Exception as e:
            logging.info("[Shell] Cannot shutdown client connection : %s" %(e))

   def buildResponse(self):
      response = ""
      try:
         opcode,args = self.cmd.split(' ', 1)
      except ValueError:
         opcode = self.cmd.rstrip()
         args = None
      try:
         #for debug purposes
         """
         print handlers[opcode]['fun'].__name__
         print handlers[opcode]['fun'].__class__
         print handlers[opcode]['fun'].__dict__
         print args
         """
         if (args):
            args.rstrip('\r\n')
         response = handlers[opcode]['fun'](args)  #call the handler
      except KeyError as e:
         response = "Unknown command '%s'" %(opcode)
      except Exception as e:
         response = "%s" %(e)
      return response

###### plugin definition ######
class shellPlugin(plugin_def.Plugin):
   def __init__(self):
      """
      Calling super's constructor is needed, to create Metis' Plugin internal structure
      """
      super(shellPlugin,self).__init__(PLUGIN_NAME)
      """
      Then we register all Actions and Events this plugin can trigger
      """
      self.addEvent(ShellCmdEvent())
      """
      Set default preferences values
      """
      self.poll_interval = 2 # only polls for shutdown, not for incoming requests
      #do not create Metis users in a plugin's __init__!! (it should be done in run)

   """
   Here's the main code of the plugin
   This is executed inside the plugin's own thread
   """
   def run(self):
      u = userModule.getUserByName(PLUGIN_USERNAME)
      if (u == None):
         u = userModule.createNewUser(PLUGIN_USERNAME)

      self.server = SocketServer.TCPServer((PLUGIN_HOST, PLUGIN_PORT), shell)
      logging.warning("ShellPlugin starts")
      self.server.serve_forever(self.poll_interval)
      logging.warning("ShellPlugin ends")

   def stop(self):
      self.server.shutdown() #beware the blocking shutdown()...

