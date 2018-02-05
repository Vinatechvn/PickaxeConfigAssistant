#
#	I M P O R T S
import os
import json
import time
import re
import random
import numpy as np
import matplotlib.pyplot as plt
import util
import signal
from subprocess import Popen
#
#
#	P I C K A X E  C O N F I G  G E N E R A T O R
#	Pickaxe Config Assistant
#
#	A class that can run an instance of XMRig, analyse the log and save into a json
#	file. This json file is then graphed using matplotlib and saved as a png file.
#
#	TODO Use a config.json file to hand in args.
#
class PickaxeConfigAssistant():
	#
	#	Constructor
	def __init__(self, **kwargs):
		print("Creating new PickaxeConfigAssistant()")
		self.mode = {"mining_software":"xmrig", "gpu_type":"nvidia"}
		#
		#	Read our gpu type input
		self.mode["gpu_type"] = kwargs.get("mode", "nvidia")
		self.gpu_name = "GPU #0"
		self.gpu_clocks = {"core":0, "memory":0}
		self.version_number = 142662
		#
		#	Settings for XMRig
		self.index = kwargs.get("index", 0)		
		self.affine_to_cpu = kwargs.get("affine_to_cpu", 0)
		#
		#	AMD XMRig Settings
		self.intensity = kwargs.get("intensity", 64)
		self.intensity_min = kwargs.get("intensity_min", self.intensity)
		self.intensity_max = kwargs.get("intensity_max", self.intensity)
		self.intensity_step = kwargs.get("intensity_step", 16)
		self.worksize = kwargs.get("worksize", 4)
		self.worksize_min = kwargs.get("worksize_min", self.worksize)
		self.worksize_max = kwargs.get("worksize_max", self.worksize)
		self.worksize_step = kwargs.get("worksize_step", 1)
		self.worker_threads = kwargs.get("worker_threads", 1)
		#
		#	NVIDIA XMRig Settings
		self.thread_count = kwargs.get("thread_count", 1)
		self.block_count = kwargs.get("block_count", 1)
		self.bfactor = kwargs.get("bfactor", 12)
		self.bsleep = kwargs.get("bsleep", 25)
		self.block_count_min = kwargs.get("block_count_min", self.block_count)
		self.thread_count_min = kwargs.get("thread_count_min", self.thread_count)
		self.thread_count_max = kwargs.get("thread_count_max", self.thread_count)
		self.block_count_max = kwargs.get("block_count_max", self.block_count)
		self.thread_count_step = kwargs.get("thread_count_step", 1)
		self.block_count_step = kwargs.get("block_count_step", 1)
		#
		#	Settings for the main loop
		self.benchmark_mining_seconds = kwargs.get("benchmark_mining_seconds", 42)
		#
		#	Internal functionality settings
		self.xmrig_version = ""
		self.ANALYSIS_OBJECTS = []
		self.is_continue = True
		self.path_xmrig_root_nvidia = ".{}xmrig-nvidia{}".format(os.sep, os.sep)
		self.path_xmrig_root_amd = ".{}xmrig-amd{}".format(os.sep, os.sep)
		#util.mkdir(self.path_xmrig_root_nvidia)
		self.path_logs_folder = ".{}logs{}".format(os.sep, os.sep)
		self.filename_xmrig_exe_nvidia = "xmrig-nvidia"
		self.filename_xmrig_exe_amd = "xmrig-amd"
		if os.name == 'nt':
			self.filename_xmrig_exe_nvidia += ".exe"
			self.filename_xmrig_exe_amd += ".exe"
		self.filename_xmrig_config = "config.json"
		self.filename_xmrig_log = "log.txt"
		self.path_results_folder = ".{}".format(os.sep)
		self.path_results_file = "results.json"
		#
		#	Graph settings
		self.x_inches_width = 9
		self.x_inches_width_min = 9
		self.y_inches_height = 12
		self.y_inches_height_min = 12
		self.bar_width = 0.5
		self.background_colour = "#FEFBD0"
		self.bar_colour = "#8AB9AE"
		self.bar_colour_max ="#8AB9AE"
		self.bar_colour_min = "#F4828C"
		self.bar_colour_average = "#775D6A"
		self.bar_colour_wattage = "#ACBD86"
		#util.mkdir(self.path_results_folder)
		#
		#	Regex
		self.regex_hash_rate_second = r"15m \d+.\d"
		self.regex_wattage = r"\d+W"
		self.regex_card_name_nvidia = r"\d:       .+@"
		self.regex_card_name_amd = r"GPU #\d.+,"
		self.regex_card_clocks = r"@ \d+\/\d+"
		self.regex_xmrig_version = r"XMRig\S+"

	#
	#	Represent the current thread_string data as our print()
	def __str__(self):
		return json.dumps(self.generate_thread_setting_object())

	#
	#	Get the total number of loops the application will be active for
	def calculate_total_number_of_iterations(self):
		if self.mode["gpu_type"] == "nvidia":
			#
			#	Handle Nvidia : threads & blocks
			thread_loops = 1 + (self.thread_count_max / self.thread_count_step - self.thread_count_min / self.thread_count_step)
			block_loops = 1 + (self.block_count_max / self.block_count_step - self.block_count_min / self.block_count_step)
			return thread_loops * block_loops
		if self.mode["gpu_type"] == "amd":
			#
			#	Handle AMD : intensity & work size
			intensity_loops = 1 + (self.intensity_max / self.intensity_step - self.intensity_min / self.intensity_step)
			worksize_loops = 1 + (self.worksize_max / self.worksize_step - self.worksize_min / self.worksize_step)
			return intensity_loops * worksize_loops

	#
	#	M A I N L I N E
	#
	#	Run the instances of XMRig with the given inputs and gather data from the log
	#	after the given benchmark seconds.
	def run_analysis(self):
		#
		#	Make a folder to store our results
		self.path_results_folder = ".{}analysis{}{}-{}{}".format(os.sep, os.sep, util.random_string(8), self.mode["gpu_type"], os.sep)
		util.mkdir(self.path_results_folder)
		#
		#	Clear the old XMRig log file
		util.write_file(self.get_xmrig_log_file_path(), "")
		#
		#	Print estimated run time
		estimated_run_time = self.benchmark_mining_seconds * self.calculate_total_number_of_iterations()
		print("Estimated run time: {} minutes".format(int(estimated_run_time / 60)))
		#
		#	While we are within the limits of all of our settings, iterate
		is_first_iteration = True
		while self.is_continue:
			#
			#	Save our config to the XMRis' config.txt
			self.update_xmrig_config_json_with_threads_object(
				self.generate_thread_setting_object())
			#
			#	Run this computation with the given settings we just updated
			if self.mode["gpu_type"] == "nvidia":
				print("Starting XMRig-{} with threads:{} blocks:{} ({}x{})".format(self.mode["gpu_type"], self.thread_count, 
					self.block_count, self.thread_count, self.block_count))
			if self.mode["gpu_type"] == "amd":
				print("Starting XMRig-{} with intensity:{} worksize:{} ({}x{})".format(self.mode["gpu_type"], self.intensity, 
					self.worksize, self.intensity, self.worksize))
			#
			#	Start XMRig using subprocess
			self.run_xmrig()
			#
			#	Update our GPU Name if it is not already set
			if is_first_iteration:
				self.gpu_name = self.read_gpu_name_from_xmrig_log()
				self.gpu_clocks = self.read_gpu_clocks_from_xmrig_log()
				#
				#	Might as well read the XMRig version here too
				self.xmrig_version = self.read_xmrig_version_from_xmrig_log()
				is_first_iteration = False
			#
			#	Analyse the results
			analysis_object = self.analyse_xmrig_log_returning_object(
				self.get_xmrig_log_file_path())
			#
			#	Create the information object (TEMP)
			information_object = {
				"GPU": self.gpu_name,
				"GPUType": self.mode["gpu_type"],
				"XMRigVersion": self.xmrig_version,
				"CompletedAt": time.time()
			}
			#
			#	Assemble what we need to store for metrics/info/graphing
			final_object = {
				"config": self.generate_thread_setting_object(),
				"analysis": analysis_object,
				"information": information_object
			}
			#
			#	Save the results to the database
			self.ANALYSIS_OBJECTS.append(final_object)
			#
			#	Write the results to file
			json_analysis_objects = json.dumps(self.ANALYSIS_OBJECTS, indent=4, 
				separators=(',', ': '))
			util.write_file(self.get_results_file_path(), json_analysis_objects)
			
			#
			#	Clear the old XMRig config file
			util.write_file(self.get_xmrig_log_file_path(), "")
			#
			#	End of the loop, let's update our config and check all the rules
			self.continue_this_computation()



	

	


	
	#
	#	D A T A  F U N C T I O N S
	#
	#	Basic getter/setters
	def get_xmrig_config_file_path(self):
		if self.mode["gpu_type"] == "nvidia":
			return self.path_xmrig_root_nvidia + self.filename_xmrig_config
		if self.mode["gpu_type"] == "amd":
			return self.path_xmrig_root_amd + self.filename_xmrig_config
	def get_xmrig_log_file_path(self):
		return self.path_logs_folder + self.filename_xmrig_log
	def get_results_file_path(self):
		return self.path_results_folder + self.path_results_file
	#
	#	Create a Thread object to model our settings
	def generate_thread_setting_object(self):
		thread_objects = []
		if self.mode["gpu_type"] == "nvidia":
			thread_obj = {
				"index": self.index,
				"threads": self.thread_count,
				"blocks": self.block_count,
				"bfactor": self.bfactor,
				"bsleep": self.bsleep,
				"affine_to_cpu": self.affine_to_cpu
			}
			thread_objects.append(thread_obj)
		if self.mode["gpu_type"] == "amd":
			thread_obj = {
				"index": self.index,
				"intensity": self.intensity,
				"worksize": self.worksize,
				"affine_to_cpu": self.affine_to_cpu
			}
			for i in range(0, self.worker_threads):
				thread_objects.append(thread_obj)
		#
		#	Returns a list
		return thread_objects
	#
	#	If we have iterated through all thread/block inputs end,
	#	else, add a thread/block to the count
	def continue_this_computation(self):
		if self.mode["gpu_type"] == "nvidia":
			if self.thread_count < self.thread_count_max:
				#
				#	We can add more threads still, let's do that
				self.thread_count += self.thread_count_step
			else:
				#
				#	We completed this run of threads, so let's increment the blocks
				if self.block_count == self.block_count_max:
					#
					#	We are done, exit
					self.is_continue = False
				else:				
					self.thread_count = self.thread_count_min
					self.block_count += self.block_count_step
			return self.is_continue
		#
		#	AMD cards
		if self.mode["gpu_type"] == "amd":
			if self.intensity < self.intensity_max:
				#
				#	We can add more threads still, let's do that
				self.intensity += self.intensity_step
			else:
				#
				#	We completed this run of threads, so let's increment the blocks
				if self.worksize == self.worksize_max:
					#
					#	We are done, exit
					self.is_continue = False
				else:				
					self.intensity = self.intensity_min
					self.worksize += self.worksize_step
			return self.is_continue










	#
	#	X M R I G  C O N F I G  F U N C T I O N S
	#
	#	Read the GPU name from an XMRig log
	def read_gpu_name_from_xmrig_log(self):
		#
		#	Need another function for AMD - todo
		gpu_name_string = "GPU #{}".format(self.index)
		xmrrig_log_file_contents = util.read_file(self.get_xmrig_log_file_path())
		gpu_name_search = ""
		#
		#	Need to update these, it's pretty coarse
		if self.mode["gpu_type"] == "nvidia":
			gpu_name_search = re.finditer(self.regex_card_name_nvidia, xmrrig_log_file_contents)
			for matchNum, match in enumerate(gpu_name_search):
				gpu_name_string = (match.group().split("       ")[1])[:-2]		
		if self.mode["gpu_type"] == "amd":
			gpu_name_search = re.finditer(self.regex_card_name_amd, xmrrig_log_file_contents)
			for matchNum, match in enumerate(gpu_name_search):
				gpu_name_string = match.group().split("), ")[0].split("(")[1]
		
		return gpu_name_string
	#
	#	Read the Core and Memory clocks from XMRig (we only see this on some cards)
	def read_gpu_clocks_from_xmrig_log(self):
		#
		#	Need another function for AMD - todo
		gpu_clocks = {
			"core":0,
			"memory":0
		}
		xmrrig_log_file_contents = util.read_file(self.get_xmrig_log_file_path())
		gpu_clocks_search = re.finditer(self.regex_card_clocks, xmrrig_log_file_contents)
		for matchNum, match in enumerate(gpu_clocks_search):
			gpu_clocks_string = match.group()[2:]
			gpu_clocks = {
				"core": gpu_clocks_string.split("/")[0],
				"memory": gpu_clocks_string.split("/")[1]
			}		
		return gpu_clocks

	#
	#	Read the version of XMRig that was used and save it to self
	def read_xmrig_version_from_xmrig_log(self):
		xmrig_version_string = "Unknown Version"
		xmrrig_log_file_contents = util.read_file(self.get_xmrig_log_file_path())
		xmrig_version_search = re.finditer(self.regex_xmrig_version, xmrrig_log_file_contents)
		for matchNum, match in enumerate(xmrig_version_search):
			xmrig_version_string = match.group().split("XMRig/")[1]
		return xmrig_version_string

	#
	#	A function to update XMRig's config.json file with a given threads object
	def update_xmrig_config_json_with_threads_object(self, threads_object):
		#
		#	Read the existing file
		if os.path.isfile(self.get_xmrig_config_file_path()):
			xmrig_config_json = json.loads(util.read_file(self.get_xmrig_config_file_path()))
			xmrig_config_json["threads"] = threads_object
			#
			#	Update with our requirements for metrics
			xmrig_config_json = self.update_generic_xmrig_config_json(xmrig_config_json)
			#
			#	Write back to disk
			xmrig_config_json_string = json.dumps(xmrig_config_json, indent=4, separators=(',', ': '))
			util.write_file(self.get_xmrig_config_file_path(), xmrig_config_json_string)
		else:
			print("could not locate config file: {}".format(self.get_xmrig_config_file_path()))

	#
	#	A function to update some sections of the XMRig config we need
	def update_generic_xmrig_config_json(self, xmrig_config_json):
		xmrig_config_json["log-file"] = self.get_xmrig_log_file_path()
		xmrig_config_json["print-time"] = 1

		return xmrig_config_json

	#
	#	A function that will analyse an XMRig log file and return an object
	def analyse_xmrig_log_returning_object(self, path):
		#
		#	Data store
		hash_rate_object = {
			"total_results":0,
			"max_hash_rate":0,
			"min_hash_rate":1000000000,
			"average_hash_rate":0,
			"average_wattage": 0
		}
		#
		#	Read the file
		#print(path)
		if os.path.isfile(path):
			xmrrig_log_file_contents = util.read_file(path)
			#print(xmrrig_log_file_contents)
			#
			#	For every line
			objs = []
			hash_rates_list = []
			wattages_list = []
			#
			#	Ok, let's grab our arrays
			hash_rates = re.finditer(self.regex_hash_rate_second, xmrrig_log_file_contents)
			wattages = re.finditer(self.regex_wattage, xmrrig_log_file_contents)
			#
			#	Create simple lists from our regex elements
			for matchNum, match in enumerate(hash_rates):
				hash_rates_list.append(float(match.group().split("15m ")[1]))
			for matchNum, match in enumerate(wattages):
				wattages_list.append(int(match.group().replace("W", "")))

			#
			#	Do we have results?
			if len(hash_rates_list) > 0:			
				#
				#	For every hashrate reading, get the value	
				for i in range(0, len(hash_rates_list)):
					if hash_rates_list[i] > hash_rate_object["max_hash_rate"]:
						hash_rate_object["max_hash_rate"] = hash_rates_list[i]

					if hash_rates_list[i] < hash_rate_object["min_hash_rate"]:
						hash_rate_object["min_hash_rate"] = hash_rates_list[i]

					hash_rate_object["average_hash_rate"] += hash_rates_list[i]
				hash_rate_object["total_results"] = len(hash_rates_list)
				hash_rate_object["average_hash_rate"] = round(hash_rate_object["average_hash_rate"] / hash_rate_object["total_results"], 1)
				#
				#	For every wattage reading
				total = 0
				elements = 0
				for wat in wattages_list:
					if wat > 0:
						total += wat
						elements += 1
				if elements != 0:
					hash_rate_object["average_wattage"] = int(total / elements)
				else:
					hash_rate_object["average_wattage"] = 0
			else:
				hash_rate_object["min_hash_rate"] = 0
				hash_rate_object["ERROR"] = True
		return hash_rate_object











	#
	#	X M R I G  S H E L L  F U N C T I O N S
	#
	#	Run an instance of XMRig and then quit after 42 seconds
	def run_xmrig(self):
		print(self.mode)
		if self.mode["gpu_type"] == "nvidia":
			cmd_string = self.path_xmrig_root_nvidia + self.filename_xmrig_exe_nvidia
		if self.mode["gpu_type"] == "amd":
			cmd_string = self.path_xmrig_root_amd + self.filename_xmrig_exe_amd
		#
		#	Create a subprocess to run on the OS within our current context
		mining = Popen(cmd_string, shell=False)
		time.sleep(self.benchmark_mining_seconds)
		if os.name == 'nt':
			#
			#	Windows, this works well to end the process
			mining.kill()
		else:
			#
			#	Linux, end using os.kill
			os.kill(mining.pid, signal.SIGKILL)
		return True







	#	
	#	G R A P H  F U N C T I O N S
	#
	#	Save our graph to a given path/in our results folder
	def save_graph(self, path=""):
		if path == "":
			path = self.path_results_folder + "graph.png"
		#
		#	Save our data
		util.write_file(self.path_results_folder + "graph_data.json",
			json.dumps(self.generate_graph_data()))
		#
		#	Graph it and save
		self.graph(self.generate_graph_data(), path)

	#
	#	Generate a list of the data objects we'll need to render a graph
	def generate_graph_data(self):
		graph_data = []
		for f_o in self.ANALYSIS_OBJECTS:
			#
			#	As we always clone worker threads, we can take element 0 here
			if self.mode["gpu_type"] == "nvidia":
				graph_object = {
					"threads": f_o["config"][0]["threads"],
					"blocks": f_o["config"][0]["blocks"],
				}
			if self.mode["gpu_type"] == "amd":
				graph_object = {
					"intensity": f_o["config"][0]["intensity"],
					"worksize": f_o["config"][0]["worksize"],
				}
			graph_object["max"] = f_o["analysis"]["max_hash_rate"]
			graph_object["min"] = f_o["analysis"]["min_hash_rate"]
			graph_object["average"] = f_o["analysis"]["average_hash_rate"]
			graph_object["wattage"] = f_o["analysis"]["average_wattage"]
			graph_data.append(graph_object)
		return graph_data
	#
	#	Use matplotlib to create and save the graph using given input data
	def graph(self, graph_data, file_name):
		x = []
		y = []
		z = []
		a = []
		b = []
		#
		#	x -> = threads | blocks
		#	y ^^ = hashrate

		for data in graph_data:
			if self.mode["gpu_type"] == "nvidia":
				x_string = "Threads: {}\nBlocks: {}".format(data["threads"], data["blocks"])
			if self.mode["gpu_type"] == "amd":
				x_string = "Intensity: {}\nWork Size: {}".format(data["intensity"], data["worksize"])
			if self.worker_threads > 1:
				x_string = "{} (x{})\n{} (x{})".format(x_string.split("\n")[0], self.worker_threads,
					x_string.split("\n")[1], self.worker_threads)
			x.append(x_string)

			y_string = data["max"]
			y.append(y_string)

			z_string = data["min"]
			z.append(z_string)

			a_string = data["average"]
			a.append(a_string)

			b_string = data["wattage"]
			b.append(b_string)
		
		#
		#	X location for the groups
		N = len(graph_data)
		ind = np.arange(N)
		#
		#	Bar width
		self.bar_width = 0.2
		#
		#	Declare our graphing objects
		fig, ax = plt.subplots(facecolor=self.background_colour)
		ax.set_facecolor(self.background_colour)
		self.x_inches_width_min = 9
		self.x_inches_width = int(len(graph_data) * 2.75)
		self.y_inches_height = 12
		if self.x_inches_width < self.x_inches_width_min:
			self.x_inches_width = self.x_inches_width_min
		#
		#	Set the output size
		fig.set_size_inches(self.x_inches_width, self.y_inches_height)
		#
		#	Map the data to a bars object
		rectangles_max = ax.bar(ind, y, self.bar_width, color=self.bar_colour_max)
		rectangles_min = ax.bar(ind + self.bar_width, z, self.bar_width, color=self.bar_colour_min)
		rectangles_average = ax.bar(ind + self.bar_width*2, a, self.bar_width, color=self.bar_colour_average)
		rectangles_wattage = ax.bar(ind + self.bar_width*3, b, self.bar_width, color=self.bar_colour_wattage)
		#
		#	Format the graph axis markers
		ax.set_xlabel('\n\n\nPickaxe Config Assistant\nALPHA-{}'.format(self.version_number))
		ax.set_ylabel('Hashrate')
		#
		#	Assemble the header of the graph, start with the name of the card
		graph_heading_string = "{} ".format(self.gpu_name)
		#
		#	If we have valid clocks, include them
		if self.gpu_clocks["core"] != 0 and self.gpu_clocks["memory"] != 0:
			graph_heading_string += "[Core: {} MHz, Memory: {} MHz] ".format(self.gpu_clocks["core"], self.gpu_clocks["memory"])
		graph_heading_string += "- XMRig ({}) - XMR".format(self.xmrig_version)
		#
		#	Set the title/heading for this graph
		ax.set_title(graph_heading_string)
		ax.set_xticks(ind + self.bar_width*2)
		ax.set_xticklabels((x))
		#
		#
		#	Apply our labels, this should be better
		for rect in rectangles_max:
			height = rect.get_height()
			ax.text(rect.get_x() + rect.get_width()/2., 0.30*height,
				'Max\n%d' % int(height) + "H/s",
				ha='center', va='bottom')
		for rect in rectangles_min:
			height = rect.get_height()
			ax.text(rect.get_x() + rect.get_width()/2., 0.60*height,
				'Min\n%d' % int(height) + "H/s",
				ha='center', va='bottom')
		for rect in rectangles_average:
			height = rect.get_height()
			ax.text(rect.get_x() + rect.get_width()/2., 0.90*height,
				'Avg\n%d' % int(height) + "H/s",
				ha='center', va='bottom')
		for rect in rectangles_wattage:
			height = rect.get_height()
			ax.text(rect.get_x() + rect.get_width()/2., 0.5*height,
				'Power\n%d' % int(height) + "W",
				ha='center', va='bottom')
		#fig.show()
		print("Saving graph to: {}".format(file_name))
		fig.savefig(file_name, facecolor=self.background_colour, transparent=True)


