from PickaxeConfigAssistant import *

#
#	Basic Test (only Threads)
#	Runs: [28, 8], [29, 8], [30, 8]
"""
pca = PickaxeConfigAssistant(
	benchmark_mining_seconds=42, 
	thread_count=28, block_count=8, 
	thread_count_min=28, thread_count_max=30, thread_count_step=1, 
	block_count_min=8, block_count_max=8, block_count_step=2)
"""
# 1:05PM 30/01/2018 - Pass

#
#	Advanced Test (Threads + Blocks)
#	Runs: 	[28, 8], [29, 8], [30, 8], [31, 8], [32, 8],
#			[28, 10], [29, 10], [30, 10], [31, 10], [32, 10],
#			[28, 12], [29, 12], [30, 12], [31, 12], [32, 12],
"""
pca = PickaxeConfigAssistant(
	benchmark_mining_seconds=42, 
	thread_count=28, block_count=8, 
	thread_count_min=28, thread_count_max=32, thread_count_step=1, 
	block_count_min=8, block_count_max=12, block_count_step=2)
#1:05PM 30/01/2018 - Pass
"""

#
#	Advanced Test (Threads + Blocks)
#	Runs: 	[28, 8], [29, 8], [30, 8], [31, 8], [32, 8],
#			[28, 9], [29, 9], [30, 9], [31, 9], [32, 9],
#			[28, 10], [29, 10], [30, 10], [31, 10], [32, 10],
"""
pca = PickaxeConfigAssistant(
	benchmark_mining_seconds=42, 
	thread_count=28, block_count=8, 
	thread_count_min=28, thread_count_max=32, thread_count_step=1, 
	block_count_min=8, block_count_max=10, block_count_step=1)
"""
# 1:24PM 30/01/2018 - PASS

#
#	Simple test, 1x run

pca = PickaxeConfigAssistant(
	benchmark_mining_seconds=42, 
	thread_count=30, block_count=8, 
	thread_count_min=30, thread_count_max=30, thread_count_step=1, 
	block_count_min=8, block_count_max=8, block_count_step=1)

#
#	Simple test, 2x run
"""
pca = PickaxeConfigAssistant(
	benchmark_mining_seconds=42, 
	thread_count=28, block_count=8, 
	thread_count_min=28, thread_count_max=28, thread_count_step=1, 
	block_count_min=8, block_count_max=9, block_count_step=1)
"""
#
#	Intense Test 32x run
"""
pca = PickaxeConfigAssistant(
	benchmark_mining_seconds=42, 
	thread_count=32, block_count=8, 
	thread_count_min=32, thread_count_max=64, thread_count_step=1, 
	block_count_min=9, block_count_max=9, block_count_step=1)
"""

def test(pca):
	pca.run_analysis()
	pca.save_graph("TEST_1.png")
	pca.save_graph()
	print(pca)

test(pca)