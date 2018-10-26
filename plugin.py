##################################################################################
#################################### INFO ########################################
##################################################################################
#               Channel list updater by AsHeS
#
#         If you plan to improve or change this script, 
#          please contact manuel.joao.amaro@gmail.com
#
#
#  If you want to change the list links, pelase change the file servers.py ONLY
#
#          Don't alter anything here or you're on you own.
#
# 
##################################################################################
################################# Changelog ######################################
##################################################################################
#  2014-03-20 - Release 0.7
#                       - Bug display info from lists (always displaying same info)
#                        
#  2014-03-20 - Release 0.6
#                       - Minor update to urllib2 (User agent request)
#                       - Modified servers.py
#                        
#  2014-03-05 - Release 0.5
#                       - Minor Bug fixes
#                       - Corrected bug opening About menu
#                       - Corrected http links for lists
#                        
#  2014-03-04 - Release 0.4
#                       - Bug fixes
#                       - Changed servers.py to enable dynamic list creation
#                       - Read servers_new.py from server for recent changes and configuration
#                       - Display latest plugin version from server
#                       - Code rewriten
#                       
#  2014-02-26 - Release 0.3
#			- Logo updated (thanks to frodoring)
#			- Few minor tweaks (no bug changes)
#
#  2014-02-26 - Release 0.2
#                       - Minor Bug fixes
#			- Removed reboot after install
#			- Removed reboot after uninstall
#			- Added all to architectures
#
#  2014-02-25 - Release 0.1
#			
#			- First release
#			- 5 list pre-configure in servers.py
# 
#
#
#
##################################################################################
################################# TODO ###########################################
##################################################################################
#
#   * in-plugin option to configure url for listdownload (in zip format)
#
##################################################################################
##################################################################################
##################################################################################
#
#
##################################################################################
################################# IMPORTS ########################################
##################################################################################
from Screens.Screen import Screen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Screens.Standby import TryQuitMainloop                  
# Python Imports
import urllib2 
import zipfile
import datetime
import os.path
import shutil
import sys
import os
# Plugin imports
from variables import ChanUpVar
from errors import *
import servers
# try to import servers_new if exists
try:
	import servers_new
except ImportError:
	pass



##################################################################################
###################### Class for default plugin Behavior #########################
##################################################################################
class ChannelUpdater(Screen):
	skin = """
		<screen position="center,center" size="900,410" title="Channel List Updater (v. %s) by AsHeS " >
				<widget name="Connection"       position="20,10" size="700,20"	font="Regular;20"/>
				<widget name="ServerMessage"    position="20,30" size="700,20"	font="Regular;20"/>
				<widget name="ServerVersion"    position="20,50" size="700,20"	font="Regular;20"/>
				<widget name="Options"          position="20,90" size="800,20"	font="Regular;20"/>
				<widget name="ChannelUpdater"    position="20,135" size="880,230" scrollbarMode="showOnDemand" />
		                <ePixmap pixmap="skin_default/buttons/red.png" position="10,360" size="140,40" transparent="1" alphatest="on" />
                		<ePixmap pixmap="skin_default/buttons/green.png" position="160,360" size="140,40" transparent="1" alphatest="on" />
                		<ePixmap pixmap="skin_default/buttons/yellow.png" position="310,360" size="140,40" transparent="1" alphatest="on" />
                		<ePixmap pixmap="skin_default/buttons/blue.png" position="460,360" size="140,40" transparent="1" alphatest="on" />                 
				<widget name="RedExit" position="10,360" size="140,40" backgroundColor="red" valign="center" halign="center" zPosition="2" foregroundColor="white" font="Regular;20" transparent="1"/>
				<widget name="GreenOK" position="160,360" size="140,40" backgroundColor="green" valign="center" halign="center" zPosition="2" foregroundColor="white" font="Regular;20" transparent="1"/>
				<widget name="YellowInfo" position="310,360" size="140,40" backgroundColor="yellow" valign="center" halign="center" zPosition="2" foregroundColor="white" font="Regular;20" transparent="1"/>
				<widget name="BlueSetup" position="460,360" size="140,40" backgroundColor="yellow" valign="center" halign="center" zPosition="2" foregroundColor="white" font="Regular;20" transparent="1" />
		</screen>""" %ChanUpVar.version


        ##############
	# Class init #
        ##############
	def __init__(self, session, args = 0):
		print "\n[ChannelUpdater] -> PLUGIN INIT\n"
		###################################################
		# try to get servers_new.py from server if needed #
		###################################################
		try:
			if ChanUpVar.UpdatefromServer is True:
                        	print "\n[ChannelUpdater] -> updating servers_new.py from server %s\n" %(ChanUpVar.UpdatefromServer_url)
                        	# Open file to write 
                        	f = open('/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/servers_new.py','w')
                        	f.write(urllib2.urlopen(ChanUpVar.UpdatefromServer_url).read())
		                f.close()
				# Override servers.py variable with new values
				# Checked everytime plugin is opened
				if 'servers_new' in sys.modules:  
					del(sys.modules["servers_new"]) 
				reload(servers_new);
				from servers_new import *
				reload(servers_new);
				if servers_new.UpdatefromServer:
					ChanUpVar.setUpdatefromServer(servers_new.UpdatefromServer)
				if servers_new.UpdatefromServer_url:
					ChanUpVar.setUpdatefromServer_url(servers_new.UpdatefromServer_url)
				if servers_new.InfoText:
					ChanUpVar.setInfoText(servers_new.InfoText)
				if servers_new.NewVersion:
					ChanUpVar.setNewVersion(servers_new.NewVersion)
				if servers_new.ChannelLists:
					ChanUpVar.setChannelLists(servers_new.ChannelLists)
        	except Exception, ex3:
                        print "\n[ChannelUpdater] -> Error getting servers_new.py, continuing with local file\n"
                        print ex3
	
	
		# The parameter session (provided by __init__) will be saved as class intern global variable self.session for further use.
		self.session = session       
		# Call initialisation function of the class including parameters self, self.session
		Screen.__init__(self, session)	

		# Get ChangeLog from server
                req = urllib2.Request(ChanUpVar.InfoText, None, ChanUpVar.useragent)
                serverInfo = urllib2.urlopen(req).read()

		print "\n[ChannelUpdater] -> Connected to server\n"
		self["Connection"] = Label(_("Server Connection     :  Connected to server"))
		# check for new version from servers.py (updated from server on plugin start)
		self["ServerMessage"] = Label(_("Server Message         :  %s")% (serverInfo))
		if (ChanUpVar.version == ChanUpVar.NewVersion): 
			self["ServerVersion"] = Label(_("Latest plugin version :  %s")% (ChanUpVar.version))
		else:
			self["ServerVersion"] = Label(_("Latest plugin version :  %s")% (ChanUpVar.NewVersion))
		# Label for list download
		self["Options"] = Label("Choose the channel list you want to download and install: ")

		# Channel lists to update
		list = []
		# Populate with links frmo servers.py array
		for i in xrange(1,len(ChanUpVar.ChannelLists)):
			list.append((ChanUpVar.ChannelLists[i][0],i))

		# Empty space
		list.append((_(" "), "null"))
		# Backup and restore options
		list.append((_(" Backup actual channels "), "backup"))
		list.append((_(" Restore from last backup"), "restore"))

		# KEY ACTIONS 
		self["ChannelUpdater"] = MenuList(list)
		self["RedExit"] = Label(_("Cancel"))
		self["GreenOK"] = Label(_("Select"))
		self["YellowInfo"] = Label(_("About"))
		self["BlueSetup"] = Label(_("Config"))
		self["myActionMap"] = ActionMap(["myActions"],
		{
			"ok": self.UpdateBouquet,    # Dreambox - Gigablue
			"save": self.UpdateBouquet,  # Dreambox 
			"green": self.UpdateBouquet, #
			"yellow": self.PluginInfo,
			"blue": self.PluginSetup,
			"cancel": self.Cancel, 
			"red": self.close
		}, -1)


	################################################
	# Called when OK is pressed in list of updates #
	################################################
	def UpdateBouquet(self):
		print "\n[ChannelUpdater] -> Update Bouquet \n"
		returnValue = self["ChannelUpdater"].l.getCurrentSelection()[1]
		print "\n[ChannelUpdater] -> returnValue: " + str(returnValue) + "\n"

		if returnValue is not None:
			if returnValue is "null":
				print ""
			# If is integer, then is option from the list 
			elif self.isInt(returnValue):
				self.downloadList(returnValue)
			# do backup
			elif returnValue is "backup":
				self.session.openWithCallback(self.backup, MessageBox, _("Do you want to backup your actual channel settings ?"), MessageBox.TYPE_YESNO)
			# do restore
			elif returnValue is "restore":
				last = None
				last = self.checkLastBackup()
				if last is not None:
					self.session.openWithCallback(self.restore, MessageBox, _("Last backup: %s\n\nDo you want to restore your channel settings with the last backup ?") %last, MessageBox.TYPE_YESNO)
				else:
					self.session.open(MessageBox,_("Sorry. No backups available."), MessageBox.TYPE_ERROR)
			else:
				print "\n[ChannelUpdater] [Bouquet] -> Cancel\n"
				self.close(None)


	#######################################################################################################################################
	#######################################################################################################################################
	#######################################################################################################################################

	#####################################################################
	#   Called when option is chosen in list - download an store file   #
	#####################################################################
	def downloadList(self, returnValue):	
		try:
			List_Link      = ChanUpVar.ChannelLists[returnValue][1]	# Link to zip file
			ChangeLog_Link = ChanUpVar.ChannelLists[returnValue][2]	# Link to list changelog

			print "\n[ChannelUpdater] -> Checking changelog for this zip (if available on server) - "+str(ChangeLog_Link)+"\n"	
			ret = urllib2.urlopen(ChangeLog_Link)
			print "\n[ChannelUpdater] -> Checking changelog returned: "+str(ret.code)+"\n"	
			# Check if link exists
			if ret.code == 200:
                		req = urllib2.Request(ChangeLog_Link, None, ChanUpVar.useragent)
                		List_ChangeLog = urllib2.urlopen(req).read()
			else:
				List_ChangeLog = "No changelog available"
			print "\n[ChannelUpdater] -> Changelog is : "+str(List_ChangeLog)+"\n"	
			print "\n[ChannelUpdater] -> Deleting old temp files\n"	
			if os.path.isfile('/tmp/list.zip'):
				os.remove('/tmp/list.zip')
			# Open file to write 
			f = open('/tmp/list.zip','w')
			# Download file to /tmp/list.zip - overwriting existing file
                	req = urllib2.Request(List_Link, None, ChanUpVar.useragent)
                	f.write(urllib2.urlopen(req).read())
			f.close()
			print "\n[ChannelUpdater] -> File downloaded \n"	
			if self.unzipList():
				self.session.openWithCallback(self.installList, MessageBox, _("Changelog:\n%s\n\nFile downloaded and extracted.\n Update channel list ?") %List_ChangeLog, MessageBox.TYPE_YESNO)
			else:
				self.session.open(MessageBox,_("Error unziping file.\nPlease try again later."), MessageBox.TYPE_ERROR)
		except urllib2.HTTPError, ex2:
			print "\n[ChannelUpdater] -> There was an http error\n"
			print ex2
			self.session.open(ChannelUpdaterError)
		except urllib2.URLError, ex2:
			print "\n[ChannelUpdater] -> There was an url error\n"
			print ex2
			self.session.open(ChannelUpdaterError)
		except Exception, ex2:
			print "\n[ChannelUpdater] -> There was an http exception\n"
			print ex2
			self.session.open(ChannelUpdaterError)


	#######################################################################################################################################
	#######################################################################################################################################
	#######################################################################################################################################

	##################################################
	# Function to unzip downloaded file insinde /tmp #
	##################################################
        def unzipList(self):
                try:
                        zfile = zipfile.ZipFile("/tmp/list.zip")
                        for name in zfile.namelist():
                         (dirName, fileName) = os.path.split(name)
                         if fileName == '':
                              # directory
                              print "\n[ChannelUpdater] -> Decompressing  -> mkdir " + '/tmp/list/' + dirName
                              newDir = '/tmp/list/' + dirName
                              if not os.path.exists(newDir):
                                  os.makedirs(newDir)
                         else:
                              # file
                              print "\n[ChannelUpdater] -> Decompressing " + fileName + " on /tmp/list/" + dirName
                              fd = open('/tmp/list/' + name, 'wb')
                              fd.write(zfile.read(name))
                              fd.close()
                        zfile.close()
                        return True
                except Exception, ex3:
                        print "\n[ChannelUpdater] -> There was an error unziping file\n"
                        print ex3
                        return False


	#######################################################################################################################################
	#######################################################################################################################################
	#######################################################################################################################################

	##########################################
	# Called after download and extract list #
	##########################################
	def installList(self, result):
		try:
			print "\n[ChannelUpdater] -> Installing channel list (YES\NO)\n"
			if result:
				print "\n[ChannelUpdater] -> Installing channel list answer: YES"
				print "\n[ChannelUpdater] -> Installing channel list: removing /etc/tuxbox/satellites.xml"
				if os.path.isfile('/etc/tuxbox/satellites.xml'):
					os.remove('/etc/tuxbox/satellites.xml')
				print "\n[ChannelUpdater] -> Installing channel list: removing /etc/tuxbox/terrestrial.xml"
				if os.path.isfile('/etc/tuxbox/terrestrial.xml'):
					os.remove('/etc/tuxbox/terrestrial.xml')
				print "\n[ChannelUpdater] -> Installing channel list: removing /etc/tuxbox/cables.xml"
				if os.path.isfile('/etc/tuxbox/cables.xml'):
					os.remove('/etc/tuxbox/cables.xml')
				print "\n[ChannelUpdater] -> Installing channel list: removing /etc/enigma2/lamedb"
				if os.path.isfile('/etc/enigma2/lamedb'):
					os.remove('/etc/enigma2/lamedb')
				print "\n[ChannelUpdater] -> Installing channel list: removing /etc/enigma2/blacklist"
				if os.path.isfile('/etc/enigma2/blacklist'):
						os.remove('/etc/enigma2/blacklist')
				print "\n[ChannelUpdater] -> Installing channel list: removing /etc/enigma2/*_bak"
				filelist = [ f for f in os.listdir("/etc/enigma2/") if f.endswith("_bak") ]
				for f in filelist:
				    os.remove('/etc/enigma2/'+f)
				print "\n[ChannelUpdater] -> Installing channel list: removing /etc/enigma2/*_org"
				filelist = [ f for f in os.listdir("/etc/enigma2/") if f.endswith("_org") ]
				for f in filelist:
				    os.remove('/etc/enigma2/'+f)
				print "\n[ChannelUpdater] -> Installing channel list: removing /etc/enigma2/*.tv"
				filelist = [ f for f in os.listdir("/etc/enigma2/") if f.endswith(".tv") ]
				for f in filelist:
				    os.remove('/etc/enigma2/'+f)
				print "\n[ChannelUpdater] -> Installing channel list: removing /etc/enigma2/*.radio"
				filelist = [ f for f in os.listdir("/etc/enigma2/") if f.endswith(".radio") ]
				for f in filelist:
				    os.remove('/etc/enigma2/'+f)
				
				print "\n[ChannelUpdater] -> Installing channel list: copying satellites.xml to /etc/tuxbox/"
				for root, dirs, files in os.walk("/tmp/list/"):
				    for file in files:
					if file.endswith("satellites.xml"):
						shutil.copy2(os.path.join(root, file), '/etc/tuxbox/')	
				print "\n[ChannelUpdater] -> Installing channel list: copying terrestrial.xml to /etc/tuxbox/"
				for root, dirs, files in os.walk("/tmp/list/"):
				    for file in files:
					if file.endswith("terrestrial.xml"):
						shutil.copy2(os.path.join(root, file), '/etc/tuxbox/')	
				print "\n[ChannelUpdater] -> Installing channel list: copying cables.xml to /etc/tuxbox/"
				for root, dirs, files in os.walk("/tmp/list/"):
				    for file in files:
					if file.endswith("cables.xml"):
						shutil.copy2(os.path.join(root, file), '/etc/tuxbox/')	
				print "\n[ChannelUpdater] -> Installing channel list: copying lamedb to /etc/enigma2"
				for root, dirs, files in os.walk("/tmp/list/"):
				    for file in files:
					if file.endswith("lamedb"):
						shutil.copy2(os.path.join(root, file), '/etc/enigma2/')	
				print "\n[ChannelUpdater] -> Installing channel list: copying blacklist to /etc/enigma2"
				for root, dirs, files in os.walk("/tmp/list/"):
				    for file in files:
					if file.endswith("blacklist"):
						shutil.copy2(os.path.join(root, file), '/etc/enigma2/')	
				print "\n[ChannelUpdater] -> Installing channel list: copying *.tv to /etc/enigma2"
				for root, dirs, files in os.walk("/tmp/list/"):
				    for file in files:
					if file.endswith(".tv"):
						shutil.copy2(os.path.join(root, file), '/etc/enigma2/')	
				print "\n[ChannelUpdater] -> Installing channel list: copying *.radio to /etc/enigma2"
				for root, dirs, files in os.walk("/tmp/list/"):
				    for file in files:
					if file.endswith(".tv"):
						shutil.copy2(os.path.join(root, file), '/etc/enigma2/')	
				print "\n[ChannelUpdater] -> Removing downloaded files\n"
				if os.path.exists('/tmp/list'):
					shutil.rmtree('/tmp/list/')
				if os.path.isfile('/tmp/list.zip'):
					os.remove('/tmp/list.zip')
				# Reload lamedb => wget -qO - http://127.0.0.1/web/servicelistreload?mode=0	
				# Several ptoblem - not using
				self.session.openWithCallback(self.reboot, MessageBox, _("Channel list updated. You must restart enigma2 before the new settings will take effect.\n\n Restart enigma2 ?"), MessageBox.TYPE_YESNO)
			else:
				print "\n[ChannelUpdater] -> Installing channel list answer: NO\n"
				print "\n[ChannelUpdater] -> Removing downloaded files\n"
				if os.path.exists('/tmp/list'):
					shutil.rmtree('/tmp/list/')
				if os.path.isfile('/tmp/list.zip'):
					os.remove('/tmp/list.zip')
				self.session.open(MessageBox,_("Installation cancelled."), MessageBox.TYPE_ERROR)
		except Exception, ex3:
			print "\n[ChannelUpdater] -> There was an error installing channel list\n"
			print ex3
		
	#######################################################################################################################################
	#######################################################################################################################################
	#######################################################################################################################################

	####################################
	#    Function to check last backup #
	####################################
	def checkLastBackup(self):
		try:
			print "\n[ChannelUpdater] -> Checking last backup\n"
			last =datetime.datetime.fromtimestamp(os.path.getmtime('/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/lamedb'))
			return last
		except Exception, ex:
			print "\n[ChannelUpdater] -> There was a error checking last backup\n"

	#######################################################################################################################################
	#######################################################################################################################################
	#######################################################################################################################################

	####################################
	#    Function to backup settings   #
	####################################
	def backup(self,result):
		try:
			if result:
				print "\n[ChannelUpdater] -> Backing up enigma2 settings"
				print "\n[ChannelUpdater] -> Removing actual backup"
				if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/'):
					shutil.rmtree('/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/')
				print "\n[ChannelUpdater] -> Copying actual enigma settings"
				shutil.copytree('/etc/enigma2/','/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/')
				print "\n[ChannelUpdater] -> Copying satellites,terrestrial and cable XML files"
				if os.path.isfile('/etc/tuxbox/satellites.xml'):
					shutil.copy2('/etc/tuxbox/satellites.xml','/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/')	
				if os.path.isfile('/etc/tuxbox/terrestrial.xml'):
					shutil.copy2('/etc/tuxbox/terrestrial.xml','/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/')	
				if os.path.isfile('/etc/tuxbox/cables.xml'):
					shutil.copy2('/etc/tuxbox/cables.xml','/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/')	
				self.session.open(MessageBox,_("Backup finished.") , MessageBox.TYPE_INFO)
			else:
				self.session.open(MessageBox,_("Backup cancelled.") , MessageBox.TYPE_INFO)
		except Exception, ex:
			print "\n[ChannelUpdater] -> There was a error during backup\n"
			print ex
			self.session.open(MessageBox,_("Unexpected error during backup."), MessageBox.TYPE_ERROR)
			print ex
			return None

	#######################################################################################################################################
	#######################################################################################################################################
	#######################################################################################################################################
			
	####################################
	#    Function to restore settings #
	####################################
	def restore(self,result):
		try:
			if result:
				print "\n[ChannelUpdater] -> Restoring enigma settings\n"
				print "\n[ChannelUpdater] -> Removing old enigma settings\n"
				shutil.rmtree('/etc/enigma2')
				print "\n[ChannelUpdater] -> Copying backup settings"
				shutil.copytree('/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/','/etc/enigma2')
				print "\n[ChannelUpdater] -> Copying satellites,terrestrial and cable XML files"
				if os.path.isfile('/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/satellites.xml'):
					shutil.copy2('/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/satellites.xml','/etc/tuxbox/satellites.xml')
				if os.path.isfile('/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/terrestrial.xml'):
					shutil.copy2('/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/terrestrial.xml','/etc/tuxbox/terrestrial.xml')
				if os.path.isfile('/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/cables.xml'):
					shutil.copy2('/usr/lib/enigma2/python/Plugins/Extensions/ChannelUpdater/backup/cables.xml','/etc/tuxbox/cables.xml')
				self.session.openWithCallback(self.reboot, MessageBox, _("Restore succeed. You must restart enigma2 before the new settings will take effect.\n\n Restart enigma2 ?"), MessageBox.TYPE_YESNO)
			else:
				self.session.open(MessageBox,_("Restore cancelled.") , MessageBox.TYPE_INFO)
		except Exception, ex:
			print "\n[ChannelUpdater] -> There was a error during restore\n"
			print ex
			self.session.open(MessageBox,_("Unexpected error during retore."), MessageBox.TYPE_ERROR)
		
		
	#######################################################################################################################################
	#######################################################################################################################################
	#######################################################################################################################################

	####################################
	#  Plugin INFORMATION - Yellow key #
	####################################
	def PluginInfo(self):
	       self.session.open(MessageBox,_("Channel updater version %s by %s.\n\n\t%s\n\n%s")% (ChanUpVar.version,ChanUpVar.author,ChanUpVar.mail,ChanUpVar.www) , MessageBox.TYPE_INFO)

	#######################################################################################################################################
	#######################################################################################################################################
	#######################################################################################################################################
		
	####################################
	#  Plugin Configuration - Blue key #
	####################################
	def PluginSetup(self):
	       self.session.open(MessageBox,_("Currently under development."), MessageBox.TYPE_INFO)

	#######################################################################################################################################
	#######################################################################################################################################
	#######################################################################################################################################


	####################################
	#      Action to leave      #
	####################################
	def Cancel(self):
		print "\n[ChannelUpdater] [Main] -> Cancel\n"
		self.close(None)

	#######################################################################################################################################
	#######################################################################################################################################
	#######################################################################################################################################

	####################################
	#      Action to restart enigma    #
	####################################
	def reboot(self,result):
		if result:
			self.session.open(TryQuitMainloop, 3)


	#######################################################################################################################################
	#######################################################################################################################################
	#######################################################################################################################################

	########################################################
	#              Default isInt function                  #
	########################################################
	def isInt(self, value):
	  try:
	    int(value)
	    return True
	  except ValueError:
	    return False

#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################

########################################################
# Test connection to server - downloading InfoText url #
########################################################
def testConnection():
	# Import Info text from server
	try:
		urllib2.urlopen(ChanUpVar.InfoText)
		return True
	except ValueError, ex:
		print "\n[ChannelUpdater] -> There was a Value error"
		print ex
		return False
	except urllib2.URLError, ex:
		print "\n[ChannelUpdater] -> There was a http error"
		print ex
	return False
	

########################################################
#      Default main function - script initizalition    #
########################################################
def main(session, **kwargs):

	print "\n[ChannelUpdater] [Main] -> Start\n"
	if servers.UpdatefromServer is not None:
		ChanUpVar.setUpdatefromServer(servers.UpdatefromServer)
	if servers.UpdatefromServer_url is not None:
		ChanUpVar.setUpdatefromServer_url(servers.UpdatefromServer_url)
	if servers.InfoText is not None:
		ChanUpVar.setInfoText(servers.InfoText)
	if servers.NewVersion is not None:
		ChanUpVar.setNewVersion(servers.NewVersion)
	if servers.ChannelLists is not None:
		ChanUpVar.setChannelLists(servers.ChannelLists)

	if testConnection():	
		# If connection to servers is OK
		session.open(ChannelUpdater)
	else:
		session.open(ChannelUpdaterError)

########################################################
#              Enigma2 Plugin Description              #
########################################################
def Plugins(**kwargs):
	return PluginDescriptor(
			name="Channel List Updater v. %s" %ChanUpVar.version ,
			description="Channel List Updater by AsHeS",
			where = PluginDescriptor.WHERE_PLUGINMENU,
			icon="plugin.png",
			fnc=main)


