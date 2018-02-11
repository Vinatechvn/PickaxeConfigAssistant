#
#	I M P O R T S
import matplotlib
import util
import os
import json
from PickaxeGraphObject import *
import matplotlib.pyplot as plt
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
	foreground_colour = "#FEFBD0"
	background_colour = "#FEFBD0"
	bar_colour = "#CCCCCC"
	width = 3
	padding = width / 2.0
	bar_padding = 0.1
	#
	#	Create our object
	def __init__(self, **kwargs):
		#self.settings = self.read_settings_from_config_file()
		self.foreground_colour = kwargs.get("foreground_colour", "#182C41")
		self.background_colour = kwargs.get("background_colour", "#182C41")
		self.bar_colour = kwargs.get("bar_colour", "#406485")
		self.font_colour = kwargs.get("font_colour", "#406485")
		self.font_colour_light = kwargs.get("font_colour_light", "#CCCCCC")
		self.this_x_location = 0

	def __str__(self):
		return json.dumps(self.settings, indent=4, 
				separators=(',', ': '))






	#
	#	M A I N L I N E
	#
	#	Take the input data and render a graph using it
	def create_graph_object_from_pickaxegraphobjects_and_matplotlib_elements(self, pgo_list, matplotlib_elements):
		#
		#	Placement co-ordinates, update with each bar we want to add
		self.this_x_location = self.padding
		is_last_bar_in_dataset = True
		tick_locations = []
		tick_labels = []
		#
		#	Adding a limit on the inputs (first 100 results)
		if len(pgo_list) > 100:
			pgo_list = pgo_list[:100]
		#
		#	For every PickaxeGraphObject we were given		
		for pgo in pgo_list:
			#
			#	Add these results to matplotlib_elements (handles lists of PickaxeGraphObjects)
			res = self.update_matplotlib_with_pickaxegraphobjects_list(pgo, matplotlib_elements, self.this_x_location)
			matplotlib_elements = res[0]
			tick_locations += res[1]
			tick_labels += res[2]
			#
			#	The next bar should be located beyond the width of this one, then padded on both sides
			if isinstance(pgo, (list,)):
				#
				#	This dataset has multiple bars for each plotting
				self.this_x_location += self.width + self.bar_padding
			else:
				#
				#	Just one bar was plotted
				self.this_x_location += self.width + (self.padding * 2)				

		#
		#	Ok, we added all the bars and we have the locations of the ticks, so we just need set the remaining
		#	variables for the matplotlib graph object
		matplotlib_elements[1].set_xticks(tick_locations)
		matplotlib_elements[1].set_xticklabels(tick_labels , rotation="vertical")
		#
		#	Fit the render to the size of the rotated x labels
		min_graph_width = 9
		graph_width = len(pgo_list) * 3
		if graph_width < min_graph_width:
			graph_width = min_graph_width
		matplotlib_elements[0].set_size_inches(graph_width, 10)
		#matplotlib_elements[0]
		matplotlib_elements[0].tight_layout(pad=3) #breaks

		#matplotlib_elements[0].show()
		#input()
		return matplotlib_elements
	





	#
	#	Generate an empty matplotlib graph using some inputs
	def create_matplotlib_graph_object(self, **kwargs):
		#
		#	matplotlib - Create our graph objects and configure them
		fig, ax = plt.subplots(facecolor=kwargs.get("foreground_colour", self.foreground_colour))
		ax.set_facecolor(kwargs.get("background_colour", self.background_colour))
		#
		#	Format the graph axis markers
		ax.set_xlabel(kwargs.get("x_label", "Untitled Axis"), color=self.font_colour_light, labelpad=40) 
		ax.set_ylabel(kwargs.get("y_label", "Untitled Axis"), color=self.font_colour_light)
		ax.set_title(kwargs.get("graph_heading", "Untitled Graph"), color=self.font_colour_light)
		ax.spines["bottom"].set_color(self.font_colour)
		ax.spines["top"].set_color(self.font_colour)
		ax.spines["left"].set_color(self.font_colour)
		ax.spines["right"].set_color(self.font_colour)
		ax.xaxis.label.set_color(self.font_colour)
		ax.yaxis.label.set_color(self.font_colour)
		#ax.setp(ax.get_xticklabels(), color=self.font_colour)
		ax.tick_params(axis="x", colors=self.font_colour)
		ax.tick_params(axis="y", colors=self.font_colour)
		#
		#	[ Figure , Plotting ]
		return [fig, ax, []]

	#
	#	Read in the settings for our object from the json
	def read_settings_from_config_file(self):
		settings_string = util.read_file(self.config_filepath)
		return json.loads(settings_string)

	#
	#	A function to add a dataset to some matplotlib_elements
	def add_pickaxegraphobject_to_matplotlib_elements(self, location, pgo, matplotlib_elements):
		matplotlib_elements[2].append(matplotlib_elements[1].bar(
			location, pgo.y, self.width, color=self.bar_colour
		))
		#print(len(matplotlib_elements[2]))
		return matplotlib_elements

	#
	#	A function to add text labels for the value in a bar graph
	def add_label_markers_to_matplotlib_elements(self, pgo, matplotlib_elements):
		for bar in matplotlib_elements[2][-1]:
			height = bar.get_height()
			matplotlib_elements[1].text(bar.get_x() + bar.get_width()/2., 0.5*height,
				pgo.y_label,
				ha='center', va='bottom', rotation='vertical', color=self.font_colour_light
			)

		return matplotlib_elements

	#
	#	This function will take a list of PickaxeGraphObjects and add it to the matplotlib_elements object
	#	at the current x location. Adds labels to the graph for the value and returns the labels and 
	#	distances for the x ticks.
	def update_matplotlib_with_pickaxegraphobjects_list(self, pgo, matplotlib_elements, this_x_location):
		tick_locations = []
		tick_labels = []
		is_last_bar_in_dataset = False
		is_multiple_bars = False
		is_first_bar = True
		if isinstance(pgo, (list,)):
			is_multiple_bars = True
		else:
			pgo = [pgo]
		#
		#	For every PickaxeGraphObject (or list of PickaxeGraphObjects, add our bars)
		#	Then update the location of the next bar
		for pgoo in pgo:
			if pgoo == pgo[-1]:
				is_last_bar_in_dataset = True
			#
			#	Render this bar, we'll need to add it to a graph object
			matplotlib_elements = self.add_pickaxegraphobject_to_matplotlib_elements(self.this_x_location, pgoo, matplotlib_elements)
			#
			#	Add our label so we can read the actual value of the bar
			self.add_label_markers_to_matplotlib_elements(pgoo, matplotlib_elements)
			#
			#	Find the middle point of this section and set the tick there, add the label too
			this_x_tick_location = self.this_x_location - self.padding + (self.width / 2)

			tick_locations.append(this_x_tick_location)
			tick_labels.append(pgoo.x)
			self.this_x_location += self.width
			if is_multiple_bars:
				self.this_x_location += self.bar_padding

		return [matplotlib_elements, tick_locations, tick_labels]

	#
	#	A function to save an image of our graph to a filepath
	def save_graph(self, matplotlib_elements, filepath):
		matplotlib_elements[0].savefig(filepath, facecolor=self.background_colour, transparent=True)


	

def test():
	pg = PickaxeGraph()
	#
	#print(pg)
	data = []
	input_data_name = "Run #1 Data"
	input_data_x = "Speed #1"
	input_data_y = 876
	input_data_label_format = "m/s"

	pga = PickaxeGraphObject(input_data_name, input_data_label_format, input_data_x, input_data_y)
	data.append(pga)

	input_data_name = "Run #2 Data"
	input_data_x = "Speed #2"
	input_data_y = 735
	input_data_label_format = "m/s"

	pga = PickaxeGraphObject(input_data_name, input_data_label_format, input_data_x, input_data_y)
	data.append(pga)

	input_data_name = "Run #3 Data"
	input_data_x = "Speed #3"
	input_data_y = 666
	input_data_label_format = "m/s"
	dats = []
	pga = PickaxeGraphObject(input_data_name, input_data_label_format, input_data_x, input_data_y)
	dats.append(pga)
	input_data_name = "Acceleration #1 Data"
	input_data_x = "Acceleration #3"
	input_data_y = 41
	input_data_label_format = "m/s²"
	pga = PickaxeGraphObject(input_data_name, input_data_label_format, input_data_x, input_data_y)
	dats.append(pga)
	input_data_name = "Acceleration #2 Data"
	input_data_x = "Acceleration #4"
	input_data_y = 76
	input_data_label_format = "m/s²"
	pga = PickaxeGraphObject(input_data_name, input_data_label_format, input_data_x, input_data_y)
	dats.append(pga)
	input_data_name = "Acceleration #2 Data"
	input_data_x = "Acceleration #4"
	input_data_y = 76
	input_data_label_format = "m/s²"
	pga = PickaxeGraphObject(input_data_name, input_data_label_format, input_data_x, input_data_y)
	dats.append(pga)
	data.append(dats)


	#
	#	Run
	matplotlib_elements = pg.create_graph_object_from_pickaxegraphobjects_and_matplotlib_elements(data, pg.create_matplotlib_graph_object())
	pg.save_graph(matplotlib_elements, "tests/testgraph.png")
#
#	T E S T S 
#test()


