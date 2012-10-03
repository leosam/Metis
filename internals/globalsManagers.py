
from eventProfileManager import *
import eventEngine
import builtins as bI

######
#init
######
engine = eventEngine.EventEngine();


#we use this to register all internal plugins
def registerInternalPlugins():
   builtins = bI.builtinPlugin()
   engine.getPluginManager().registerPlugin(builtins)
   epm = EventProfileManager()
   engine.getPluginManager().registerPlugin(epm) #here's the good way to register an internal plugin


#allow people to get a reference to the EventEngine
def getEventEngine():
   return engine

