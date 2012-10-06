import logging
import userModule
import plugin_def

class PluginProfile:
   def __init__(self, user, plugin):
      self.user = user
      self.plugin = plugin
      self.prefs = {'Pref.user':self.user}
      #FIXME: get default prefs from plugin?
      self.user.addPluginProfile(self)
      self.plugin.addPluginProfile(self)
   def addPref(self, key, value):
      self.prefs[key] = value
      
