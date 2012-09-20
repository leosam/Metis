
import eventEngine
import builtins
from eventProfileManager import *

######
#init
######
engine = eventEngine.EventEngine();
builtins = builtins.builtinPlugin()

engine.getPluginManager().registerPlugin(builtins) #don't start useless thread
epm = EventProfileManager()
engine.getPluginManager().registerPlugin(epm) #here's the good way to register an internal plugin


def getEventEngine():
   return engine

