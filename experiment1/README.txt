experiment1.tcl is the ns2 simulation script for experiment 1. However, it cannot be run using "ns2 experiment1.tcl" directly
since it takes multiple command-line arguments as simulation parameters. Instead, please use "python3 run.py" since that will
automatically run the experiment using different parameters and save the result in corresponding trace files.

Once you have all the trace files, use analyze.py to analyze every trace file. It will calculate the average throughput, average
drop rate, and average round trip time for each run and strore the metrics in a csv file. plot.R is used to produce the figures
used in our report.

We didn't run our experiments on edlab2 since the generated trace files are too large to fit in the storage limit for a single
user, but all the files can run without modification on edlab2.