import os

tcp_variants = ["Reno", "Sack1"]
output_files = ["out-reno-", "out-sack-"]
queue_disciplines = ["RED", "DropTail"]
queue_sizes = [3,7,11,19,30]

for i in range(len(tcp_variants)):
	tcp_variant = tcp_variants[i]
	for queue_discipline in queue_disciplines:
		for size in queue_sizes:
			output_filename = 'exp3/'+str(queue_discipline)+'/'+output_files[i]+queue_discipline+str(size)
			cmd = 'ns A2_EXP3.tcl ' + tcp_variant + ' ' + queue_discipline + ' ' + output_filename+' '+str(size)
			os.system(cmd)