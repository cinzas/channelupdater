from Screens.Screen import Screen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Plugins.Plugin import PluginDescriptor
from Screens.Standby import TryQuitMainloop
from variables import ChanUpVar
##################################################################################
############### Class for Errors (On connect, donwload or unzip) #################
##################################################################################
class ChannelUpdaterError(Screen):
        skin = """
                <screen position="center,center" size="600,400" title="Channel List Updater (v. %s) by AsHeS" >
                                <widget name="Error"	      position="40,60" size="550,300"   font="Regular;22"/>
                </screen>""" %ChanUpVar.version

		###############
		#  Class init #
		###############
	def __init__(self, session, args = 0):
		print "\n[ChannelUpdater] -> Error Connecting to server\n"

		# The parameter session (provided by __init__) will be saved as class intern global variable self.session for further use.
		self.session = session       
		# Call initialisation function of the class including parameters self, self.session
		Screen.__init__(self, session)	

		self["Error"] = Label("\nError connecting to server.\n\nPlease try again later.\n\nPress OK or CANCEL to exit.")
		self["myActionMap"] = ActionMap(["SetupActions"],
		{
			"ok": self.close, 
			"cancel": self.close
		}, -1)


