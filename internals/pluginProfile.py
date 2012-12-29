import logging
import userModule
import plugin_def

class PluginProfile:
   def __init__(self, user, plugin):
      self.user = user
      self.plugin = plugin
      self.prefs = {'Pref.user':self.user}
      self.user.addPluginProfile(plugin, self)
      self.plugin.addPluginProfile(user, self)
   def addPref(self, key, value):
      self.prefs[key] = value
      
