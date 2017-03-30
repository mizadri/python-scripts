#!/usr/bin/env python
import sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gmean

if len(sys.argv)<2:
    print ('Usage: %s stats-file manhattan-threshold % sys.argv[0]')
    exit(0)

filename = sys.argv[1]
m_threshold = float(sys.argv[2])
sf_threshold = 0.15
colnames = ['B_manhattan','S_manhattan','SF_distance','phase']

table = pd.read_csv(filename) 
result = pd.DataFrame([], columns=colnames)

phase = 1
recent_phase_switch = False
windows = 0

phase_indexes = pd.DataFrame([],columns=['phase_start','phase_end'])
last_phase = 0

for raw_row in table.iterrows():
	i = raw_row[0]
	row=raw_row[1]

	if(i > 0):

		if (recent_phase_switch and windows>2):
			windows = 0
			recent_phase_switch=False
		elif (recent_phase_switch and windows<=2):
			windows += 1

		big_manhattan=abs(row['B_icomp_other']-previous_row['B_icomp_other'])+abs(row['B_llcreq_pki']-previous_row['B_llcreq_pki'])
		small_manhattan=abs(row['S_icomp_other']-previous_row['S_icomp_other'])+abs(row['S_llcreq_pki']-previous_row['S_llcreq_pki'])
		sf_distance=abs(row['SF']-previous_row['SF'])
		current_phase = phase

		if (recent_phase_switch==False and big_manhattan > m_threshold and sf_distance>sf_threshold):
			phase += 1
			recent_phase_switch=True
			windows=0
			s = pd.Series([last_phase, i-1],index=['phase_start','phase_end'])
			phase_indexes = phase_indexes.append(s,ignore_index=True)
			last_phase = i

		if (big_manhattan > m_threshold or small_manhattan > m_threshold):
			current_phase = -1


		s = pd.Series([big_manhattan, small_manhattan, sf_distance, current_phase], index=colnames)
		result = result.append(s, ignore_index=True)
	else:
		s = pd.Series([0, 0, 0, -1], index=colnames)
		result = result.append(s, ignore_index=True)
	
	previous_row=raw_row[1]

s = pd.Series([last_phase, i],index=['phase_start','phase_end'])
phase_indexes = phase_indexes.append(s,ignore_index=True)

table['phase'] = result['phase']
# Rows with phase=-1 are excluded because they step over the m_threshold
filtered_table = table[table['phase']>0] 
gmeans = filtered_table.groupby(['phase'],as_index=True).agg(lambda x: gmean(list(x)))


gmeans['phase_start']=phase_indexes['phase_start']
gmeans['phase_end']=phase_indexes['phase_end']
del gmeans['B_nsample']
del gmeans['S_nsample']

cols = gmeans.columns.tolist()
cols = cols[-2:] + cols[:-2]
gmeans = gmeans[cols]

## Calcular SF real - SF geometrico
colsPlot = ['SF-real','SF-gmean-phase']
plot_data = pd.DataFrame([],columns=colsPlot)

for raw_row in table.iterrows():
	row = raw_row[1]
	sf_sample = row['SF']

	if (row['phase'] > 0):
		phase = row['phase']
		sf_phase = gmeans['SF'][phase]
	else:
		sf_phase = 0

		
	s = pd.Series([sf_sample, sf_phase],index=colsPlot)
	plot_data = plot_data.append(s,ignore_index=True)

plt.plot(table.index.values,plot_data['SF-real'], linestyle='-', color='b', label='SF-real')
plt.plot(table.index.values,plot_data['SF-gmean-phase'], linestyle='-', color='r', label='SF-gmean-phase')
plt.xlabel('Instruction windows(500M ins)')
plt.legend()
plt.grid()
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}
plt.rc('font', **font)
frame = plt.gca()
plt.savefig(sys.argv[1].split('.')[0]+'.pdf')

result.to_csv( sys.argv[1].split('.')[0]+'.phases', index=False)
gmeans.to_csv( sys.argv[1].split('.')[0]+'.gmeans', index=False)