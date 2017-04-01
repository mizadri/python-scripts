#!/usr/bin/env python
import pandas as pd
import numpy as np
table=pd.read_excel("spec_juno.xlsx",sheetname="data")
csv = pd.read_csv("ctimes-juno.csv")

# Load benchmark execution time in LITTLE to a dictionary
bench_time = {}
for raw_row in csv.iterrows():
	i = raw_row[0]
	row=raw_row[1]
	bench_time[row[0]] = row[2]/1000

# Load workload composition and SF to dicitionaries
bench_SF = {}
bench_lights = {}
workloads = []
for raw_row in table.iterrows():
	i = raw_row[0]
	row=raw_row[1]

	bench_SF[row[0]] = row[1]

	if pd.notnull(row[2]):
		benchs = []
		for b in row[2].split(','):
			name = b.replace("L","").strip()
			benchs.append(name)
			bench_lights[name] = b.strip() 
		workloads.append(benchs)

# Calculate variance of SF in each workload
SF_variations = []
for w in workloads:
	array = []
	for b in w:
		array.append(bench_SF[b])
	SF_variations.append(np.var(array))

# Sort the different workloads using SF variance
wdf = pd.DataFrame()
wdf["SF_var"] = SF_variations
wdf["Workload"] = table.Workload
sortedd = wdf.sort_values("SF_var", ascending=False)

# Obtain the longest benchmark (execution time) for each workload and print the workloads ordered by SF variance
for i in sortedd.index:
	time = []
	for benchmark in workloads[i]:
		bt = bench_lights[benchmark]
		time.append(bench_time[bt]) 
		
	arr_str = "Workload %i (%.2f s): "% (i,max(time))
	for benchmark in workloads[i]:
		arr_str += bench_lights[benchmark]+"(%.2f"%bench_SF[benchmark]+') '
	print(arr_str)
