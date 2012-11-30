'''
A Config parser class
'''

from os import path
import userModule

class Config:
	'''
	The Config class is responsible for managing all configuration information related to the testbed site
	
	'''
	
	def __init__(self, pathToConfig="metis.conf"):
		'''
		Constructor
		
		@param path_to_config: path to the testbed overall configuration
		@type path_to_config: string 
		'''
		
		self.users = {}
		self.currentUser = ""
      self.currentProfile = ""
		self.path = ""
		
		if path.isfile(pathToConfig):
			
			# Good, the file exists
			self.path = pathToConfig
			
			# Now lets try to load it
			if self.__loadConf() == 0:
				raise Exception("config_unreadable")
		
		else:
			raise Exception("no_config")
			

	def getUser(self, userName):
		'''
		Returns a EventProfile list
		'''
		
		return self.users[userName]
	
	
	def lookForNode(self, node_name):
		'''
		Checks if a specific node is on the list
		'''
		
		if node_name in self.node_list.keys():
			return self.node_list[node_name]
		
		else:
			return 0
	
	
	def __loadConf(self):
		# Private method to load a configuration file at startup
		#   this is where the intelligence of Config is!!
		
		# Open the configuration file
		conf = open(self.path, 'r')
		
		if conf:
			# We can open teh configuration file, good
			
			# Parse the configuration file
			for line in conf.readlines():
				
				# Clean up the line
				line = line.strip(' \t')
				line = line.rstrip(' \t')
				
				if line:
					# Check if it is a comment
					if line.startswith("#"):
						continue

					# Check if it is a user definition
					if line.startswith("User"):
						_,userName = line.split(' ', 1)
                  u = userModule.User(userName)
						self.users[userName] = u
                  self.currentUser = userName
						continue

					# Check if it is a EventProfile definition
					if line.endswith(":"):
						val,_ = line.split(':', 1)
						eventName = val
                  e = EventProfile(eventName)
                  self.currentUser.addEventProfile(e)
                  self.currentProfile = e
						continue

					# Check if it is an uid definition
					if line.startswith("Bind"):
                  _,actionName,eventArgument,actionArgument = line.split(' :>')
                  if self.currentProfile != None:
                     a = TheEventEngine().PluginManager.getActionByName(actionName)
                     self.currentProfile.addBinding(eventArgument, a, actionArgument)
						continue

					if line.startswith("action"):
						_,val = line.split(' ', 1)
						node_ether = val
							
					if line.startswith("type"):
						_,val = line.split(' ', 1)
						node_kind = val

						
					if len(node_name) and len(node_ether) and len(node_kind):
						# Instantiate a node object
						node = Node(node_name, node_ether, node_kind)
						
						# Add to the list of nodes
						self.node_list[node_name] = node
						node_name = ""
						continue
					
					else: 
						continue
				
			return 1
		
		else:
			# Configuration file is unreadable
			return 0
