import eventProfileManager as ePM
from plugin_def import *
from plugin_mgr import *
from action_def import *
from eventProfile import *

#QUESTION : do we need a USER for internal affairs???

#INTERNAL runtime binding
#ensure the necessary internals events are binded correctly for a given user
def __bindEventToAction__(user, pluginManager, event, actionName):
   logging.info("re-binding %s to %s" %(actionName, event.name))
   prof = user.getProfileByEvent(event)
   if (prof == None):
      prof = EventProfile(event=event)
      user.addEventProfile(prof)
   else:
      logging.debug("\tALREADY FOUND profile for event %s for user %s" %(event.name, user.name))
   action_already_found = False
   action_to_add = pluginManager.getActionByName(actionName)
   if (action_to_add == None or action_to_add.name != actionName):
      raise RuntimeError("cannot find target builtinAction to bind : %s" %(actionName))
   for a in prof.actions:
      if (a.name == action_to_add.name):
         action_already_found = True
   if (not action_already_found):
      logging.debug("\taction %s not present, adding it" %(action_to_add.name) )
      prof.addAction( action_to_add )
   else:
      logging.debug("\taction %s ALREADY FOUND for event %s on user %s (no need to re-bind it)" %(action_to_add.name,event.name,user.name))
   logging.debug("\tdone re-binding" )

#Main internal function used here
#(no one should remove anything from that, because web interface is useless without it)
def __bindInternals__(user):
   PUEvent = ePM.profilesUpdated()
   __bindEventToAction__(user,ThePluginManager(),PUEvent,"updateProfilesAction")
   NUEvent = ePM.newUser()
   __bindEventToAction__(user,ThePluginManager(),NUEvent,"handleNewUserAction")

