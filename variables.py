##################################################################################
####################  Global Variables used by Plugin ############################
##################################################################################
class myVariables:

   ## Constructor
   def __init__(self):
	self.version   = "0.7" 	# Plugin version 
	self.author    = "AsHeS"  # Plugin Author
	self.mail      = "manuel.joao.amaro@gmail.com"  # Author e-mail
	self.www       = "http://sites.google.com/site/channelupdater/" #Plugin website
	self.useragent = { 'User-Agent' : 'Mozilla/5.0' }

	self.UpdatefromServer = True       # By default Update from server - From servers.py
	self.UpdatefromServer_url = None   # Url for servers_new.py - From servers.py
	self.InfoText = None               # Url for txt from server (server ChangeLog)
	self.NewVersion = self.version     # Check if new version available
	self.ChannelLists = []             # Array with lists for download

   # Methods for variable update
   def setUpdatefromServer(self,arg1):
	self.UpdatefromServer=arg1
   def setUpdatefromServer_url(self,arg1):
	self.UpdatefromServer_url=arg1
   def setInfoText(self,arg1):
	self.InfoText=arg1
   def setNewVersion(self,arg1):
	self.NewVersion=arg1
   def setChannelLists(self,arg1):
	self.ChannelLists=arg1

##################################################################################
##################################################################################
##################################################################################
global ChanUpVar
ChanUpVar = myVariables()

