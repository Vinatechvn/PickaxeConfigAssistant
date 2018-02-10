from PickaxeConfigAssistant import * 
import sys, getopt
def main(argv):
	inputfile = ''
	outputfile = ''

	#pca = PickaxeConfigAssistant()
	#
	#	Variables we'll need
	index = 0
	seconds = 42
	thread_count, thread_count_step, thread_count_min, thread_count_max = 1, 1, 1, 1
	block_count, block_count_step, block_count_min, block_count_max = 1, 1, 1, 1
	intensity = 64
	worksize = 4
	intensity_step, intensity_min, intensity_max = 16, 1, 1
	worksize_step, worksize_min, worksize_max = 1, 1, 1
	bfactor = 12
	bsleep = 25
	affine_to_cpu = 0
	worker_threads = 1
	mode = "nvidia"
	runs = []
	graph_datasets =[]


	try:
		opts, args = getopt.getopt(argv,
			"i:s:t:b:tmax:tmin:tstep:bmax:bmin:bstep:bsleep:bfactor:affinity:in:inmax:inmin:instep:ws:wsmax:wsmin:wsstep:wt:m:r:gd",
			["index=","seconds=",
			"threads=", "blocks=",
			"threadsmax=", "threadsmin=","threadsstep=",
			"blocksmax=","blocksmin=","blocksstep=",
			"bsleep=","bfactor=","affinity=", 
			"intensity=", "intensitymax=", "intensitymin=", "intensitystep=",
			"worksize=", "worksizemax=", "worksizemin=", "worksizestep=",
			"workerthreads=", "mode=", "runs=", "graph_datasets="]
		)
	except getopt.GetoptError:
		print()
		print('Usage error, please check the input syntax and try again.\nSee https://github.com/PentagonalCube/PickaxeConfigAssistant#usage for Usage Examples.\n')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-help':
			print('<usage instructions>')
			sys.exit()
		#
		#	Card Index Numbner [GPU #0] -> 0
		if opt in ("-i", "--index"):
			index = int(arg.strip())
		#
		#	Seconds to run XMrig for
		elif opt in ("-s", "--seconds"):
			seconds = int(arg.strip())
		#
		#	GPU mode
		elif opt in ("-m", "--mode"):
			mode = arg.strip()
		#
		#	Number of threads to have in our XMRig GPU worker thread
		elif opt in ("-t", "--threads"):
			thread_count = int(arg.strip())
			thread_count_min = thread_count
			thread_count_max = thread_count
		#
		#	Number of blocks to have in our XMRig GPU worker thread
		elif opt in ("-b", "--blocks"):
			block_count = int(arg.strip())
			block_count_min = block_count
			block_count_max = block_count
		#
		#	Number of intensity to have in our XMRig GPU worker thread
		elif opt in ("-in", "--intensity"):
			intensity = int(arg.strip())
			intensity_max = intensity
			intensity_min = intensity
		#
		#	Number of worksize to have in our XMRig GPU worker thread
		elif opt in ("-ws", "--worksize"):
			worksize = int(arg.strip())
			worksize_min = worksize
			worksize_max = worksize
		#
		#	Max/Min/Steps for our threads
		elif opt in ("-tmax", "--threadsmax"):
			thread_count_max = int(arg.strip())
		elif opt in ("-tmin", "--threadsmin"):
			thread_count_min = int(arg.strip())
		elif opt in ("-tstep", "--threadsstep"):
			thread_count_step = int(arg.strip())
		#
		#	Max/Min/Steps for our blocks
		elif opt in ("-bmax", "--blocksmax"):
			block_count_max = int(arg.strip())
		elif opt in ("-bmin", "--blocksmin"):
			block_count_min = int(arg.strip())
		elif opt in ("-bstep", "--blocksstep"):
			block_count_step = int(arg.strip())
		#
		#	Max/Min/Steps for our intensity
		elif opt in ("-inmax", "--intensitymax"):
			intensity_max = int(arg.strip())
		elif opt in ("-inmin", "--intensitymin"):
			intensity_min = int(arg.strip())
		elif opt in ("-instep", "--intensitystep"):
			intensity_step = int(arg.strip())
		#
		#	Max/Min/Steps for our worksize
		elif opt in ("-wsmax", "--worksizemax"):
			worksize_maxi = int(arg.strip())
		elif opt in ("-wsmin", "--worksizemin"):
			worksize_min = int(arg.strip())
		elif opt in ("-wsstep", "--worksizestep"):
			worksize_step = int(arg.strip())
		#
		#	Map this process to a specific CPU core?
		elif opt in ("-affinity", "--affinity"):
			affine_to_cpu = arg.strip()
		#
		#	Interval to sleep the XMRig process (on the kernel?)
		elif opt in ("-bsleep", "--bsleep"):
			bsleep = int(arg.strip())
		#
		#	Level of aggression when getting tome on the kernel?
		elif opt in ("-bfactor", "--bfactor"):
			bfactor = int(arg.strip())
		#
		#	The number of threads to run in parallel (AMD) (cloned threads)
		elif opt in ("-th", "--workerthreads"):
			worker_threads = int(arg.strip())
		#
		#	A way to give specific inputs into the application "[80x3, 60x8, 20x2]"
		#	Must be a string input
		elif opt in ("-r", "--runs"):
			runs = arg.strip()
			runs = runs.replace("[", "")
			runs = runs.replace("]", "")
			runs = runs.split(",")
			all_runs = []
			for run in runs:
				a = int(run.split("x")[0].strip())
				b = int(run.split("x")[1].strip())
				all_runs.append({
					"a": a,
					"b": b
				})
			runs = all_runs

		elif opt in ("-gd", "--graph_datasets"):
			graph_datasets = arg.strip()
			graph_datasets = graph_datasets.replace("[", "")
			graph_datasets = graph_datasets.replace("]", "")
			graph_datasets = graph_datasets.split(",")
			grap_datasets = []
			for i in graph_datasets:
				grap_datasets.append(i.strip())
			graph_datasets = grap_datasets
			#print(graph_datasets)
			


	#
	#	With all of these settings, let's generate our Pickaxe object
	pca = PickaxeConfigAssistant(
		index=index,
		benchmark_mining_seconds=seconds,
		thread_count=thread_count, thread_count_min=thread_count_min, 
		thread_count_max=thread_count_max, thread_count_step=thread_count_step,
		block_count=block_count, block_count_min=block_count_min, 
		block_count_max=block_count_max, block_count_step=block_count_step,
		affine_to_cpu=affine_to_cpu, bfactor=bfactor, bsleep=bsleep,
		intensity=intensity, worksize=worksize,
		intensity_max=intensity_max, intensity_min=intensity_min, intensity_step=intensity_step,
		worksize_max=worksize_max, worksize_min=worksize_min, worksize_step=worksize_step,
		worker_threads=worker_threads, mode=mode, runs=runs, graph_datasets=graph_datasets
	)
	#
	#	R U N 
	pca.run_analysis()
	#pca.save_graph()
	pca.new_save_graph()

if __name__ == "__main__":
	main(sys.argv[1:])


# python main.py --index 0 --threads 30 --blocks 8 --affinity 0 --bsleep 25 --bfactor 12 --seconds 42 | OK
# python main.py --index 3 --threads 30 --blocks 8 --affinity 1 --bsleep 25 --bfactor 12 --seconds 42 | OK
# python main.py --index 0 --threads 30 --blocks 8 --affinity 1 --bsleep 25 --bfactor 12 --seconds 42 --threadsmax=32 --threadsstep=1 --blocksmax=8
# python main.py --index 0 --threads 28 --blocks 8 --affinity 1 --bsleep 25 --bfactor 12 --seconds 42 --threadsmax=32 --threadsstep=1 --blocksmax=10 --blocksstep=1
#
#	Single run
# python main.py --index 0 --threads 30 --blocks 8 --affinity 1 --bsleep 25 --bfactor 12 --seconds 42 --threadsmax=30 --threadsstep=1 --blocksmax=8