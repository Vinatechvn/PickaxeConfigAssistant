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
	bfactor = 12
	bsleep = 25
	affine_to_cpu = 0
	thread_count = 8


	try:
		opts, args = getopt.getopt(argv,
			"i:s:t:b:tmax:tmin:tstep:bmax:bmin:bstep:bsleep:bfactor:affinity",
			["index=","seconds=","threads=", "blocks=","threadsmax=", "threadsmin=","threadsstep=","blocksmax=","blocksmin=","blocksstep=","bsleep=","bfactor=","affinity="]
		)
	except getopt.GetoptError:
		print()
		print('test.py -i <inputfile> -o <outputfile>')
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
	#	With all of these settings, let's generate our Pickaxe object
	pca = PickaxeConfigAssistant(
		index=index,
		benchmark_mining_seconds=seconds,
		thread_count=thread_count, thread_count_min=thread_count_min, 
		thread_count_max=thread_count_max, thread_count_step=thread_count_step,
		block_count=block_count, block_count_min=block_count_min, 
		block_count_max=block_count_max, block_count_step=block_count_step,
		affine_to_cpu=affine_to_cpu, bfactor=bfactor, bsleep=bsleep
	)
	#print(pca)

	#
	#	R U N 
	pca.run_analysis()
	pca.save_graph()

if __name__ == "__main__":
	main(sys.argv[1:])


# python main.py --index 0 --threads 30 --blocks 8 --affinity 0 --bsleep 25 --bfactor 12 --seconds 42 | OK
# python main.py --index 3 --threads 30 --blocks 8 --affinity 1 --bsleep 25 --bfactor 12 --seconds 42 | OK
# python main.py --index 0 --threads 30 --blocks 8 --affinity 1 --bsleep 25 --bfactor 12 --seconds 42 --threadsmax=32 --threadsstep=1 --blocksmax=8
# python main.py --index 0 --threads 28 --blocks 8 --affinity 1 --bsleep 25 --bfactor 12 --seconds 42 --threadsmax=32 --threadsstep=1 --blocksmax=10 --blocksstep=1
#
#	Single run
# python main.py --index 0 --threads 30 --blocks 8 --affinity 1 --bsleep 25 --bfactor 12 --seconds 42 --threadsmax=30 --threadsstep=1 --blocksmax=8