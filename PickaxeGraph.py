#
#	I M P O R T S
import matplotlib
import util
import os
import json

#
#	W I P 



#
#
#	P I C K A X E  G R A P H
#	Pickaxe Graph
#
#	This class will handle graph creation using matplotlib. Able to create 
#	graphs from somewhat abstract datasets.
class PickaxeGraph():
	config_filepath = ".{}graphconfig.json".format(os.sep)
	settings = []
	#
	#	Create our object
	def __init__(self):
		self.settings = self.read_settings_from_config_file()

	def __str__(self):
		return json.dumps(self.settings, indent=4, 
				separators=(',', ': '))

	#
	#	Read in the settings for our object from the json
	def read_settings_from_config_file(self):
		settings_string = util.read_file(self.config_filepath)
		return json.loads(settings_string)

	#
	#	Setup the bars


	#
	#	Handle the input from the user
	


pg = PickaxeGraph()

print(pg)