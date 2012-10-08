'''
A Config parser class
'''

from os import path
from Node import Node

class Config:
	'''
	The Config class is responsible for managing all configuration information related to the testbed site
	
	'''
	
	def __init__(self, path_to_config="/etc/minus/site.conf"):
		'''
		Constructor
		
		@param path_to_config: path to the testbed overall configuration
		@type path_to_config: string 
		'''
		
		self.node_list = {}
		self.path = ""
		self.siteName = ""
		self.siteUid = ""
		
		if path.isfile(path_to_config):
			
			# Good, the file exists
			self.path = path_to_config
			
			# Now lets try to load it
			if self.__loadConf() == 0:
				raise Exception("config_unreadable")
		
		else:
			raise Exception("no_config")
			
	
	def getSiteName(self):
		'''
		Returns the site's name
		'''
		
		return self.siteName
	
	
	def getSiteUid(self):
		'''
		Returns the site's uid
		'''
		
		return self.siteUid
	
	
	def getNodeList(self):
		'''
		Returns a Node list
		'''
		
		return self.node_list.values()
	
	
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
				line = line.strip()
				line = line.rstrip()
				
				if line:
					# Check if it is a comment
					if line.startswith("#"):
						continue

					# Check if it is a name definition
					if line.startswith("name"):
						_,val = line.split(' ', 1)
						self.siteName = val
						continue
					
					# Check if it is an uid definition
					if line.startswith("uid"):
						_,val = line.split(' ', 1)
						self.siteUid = val
						continue
					
					# Check if it is a node definition
					if line.endswith(":"):
						val,_ = line.split(':', 1)
						node_name = val
						node_ether = ""
						node_kind = ""
						continue
							
					if line.startswith("mac"):
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
