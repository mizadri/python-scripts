#!/usr/bin/env python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib 
from matplotlib.markers import *
import sys
import re
import getopt
import os.path

#import seaborn
#seaborn.set()

# -p p1,p2,p3,..,pn : Patterns for each column ---> '#cccccc:/,...."
# -y y-range: ej: 1:4.20 or 1:4.20:0.1 (Increment is at the end) ----> yticks_fixed=np.arange(0,1.1,0.1)
def usage(help):
	print """Usage: %s -i data_file [options]
---Option List---
-i <input-file>: Input data file(excel or csv).
-s <sheet name>: Excel sheet to obtain the data from.
-d <width,height>: Dimensions.
-c <c1,c2,..,cn>: Column's names to remove.
-p <p1,p2,..,pn> : Patterns for each column.
-y <start,end[,step]>: ej: 1:4.20 or 1:4.20:0.1 (Increment is at the end).
-P : Enable percentage format on y axis.
-l <ylabel>: set labels for y axis.
-t <tag>: Tag that will be appended to the filename of the figure.
-r <offset_x>: Rotate x titles by 90 degrees and apply offset to separate them from the x axis.
-n : no key.
-f <fontspec>
-R <row_selection>
-A : compute average.
-h : help"""% sys.argv[0]

	if not help:
		exit(1)
	else:
		exit(0)           

try:
	opts, args = getopt.getopt(sys.argv[1:], "i:s:d:c:p:y:kl:t:r:n:f:R:Ah",
											 ["input-file","sheet","dimensions","columns","patterns"
											 ,"yrange","percentages","ylabels","tag","roffset"
											 ,"nokey","font","rows","average","help"])
except getopt.GetoptError as err:
	# print help information and exit:
	print str(err) # will print something like "option -a not recognized"
	usage(False)
	sys.exit(2)


infile = "example.xlsx"
sheet = None
figSize = [7.75,6.75]
columns = None
patterns = []
yrange = None
percentages = False
ylabels = []
tag = None
roffset = 0
nokey = False
font = "Helvetica"
rows = []
average = False

ystart = None
yend = None
ystep = None

for o, arg in opts:
	if o in ("-i", "--input"):
		infile=arg 
		assert os.path.isfile(infilen), "Specify an existing input file: -i example.xlsx" 
	if o in ("-s", "--sheet"):
		sheet=arg 
	elif o in ("-d", "--dimensions"):
		figSize = [float(d) for d in arg.split(',')]
		assert len(figSize)==2, "The dimmension has to be expressed in the following format: -d 7.75,6.75"
	elif o in ("-c", "--columns"):
		columns = arg.split(',')
	elif o in ("-p", "--patterns"):
		for coldesign in arg.split(','):
			patterns.append(coldesign.split(':'))
	elif o in ("-y", "--yrange"):
		infile=yrange
		yrange = arg.split(":")
		assert len(yrange)==2 or len(yrange)==3, "yrange should have this format: 1:4.20 or 1:4.20:0.1"
		ystart = yrange[0]
		yend = yrange[1]
		ystep = yrange[2]
	elif o in ("-P", "--percentages"):
		percentages=True
	elif o in ("-l", "--ylabels"):
		ylabels=arg
	elif o in ("-t", "--tag"):
		tag=arg
	elif o in ("-r", "--roffset"):
		roffset=float(arg)
	elif o in ("-n", "--nokey"):
		nokey=True
	elif o in ("-f", "--font"):
		font=arg
	elif o in ("-R", "--rows"):
		rows=arg
	elif o in ("-A", "--average"):
		average=True
	if o in ("-h", "--help"):
		usage(True)
		sys.exit()
	else:
		assert False, "unhandled option"

if ".csv" in infile:
	table=pd.read_csv(infile)
else:
	if sheet:
		table=pd.read_excel(infile, sheetname=sheet)
	else:
		table=pd.read_excel(infile)

nCols = len(table.columns) - 1

# Create the plot
ax=table.plot(kind='bar')
plt.figure(figsize=figSize)

# Filter columbs by name
if columns:
	table.drop(columns,axis=1,inplace=True)
	nCols -= len(columns)

if yrange:
	plt.yticks(np.arrange(ystart,yend,ystep))



# vals = ax.get_yticks()
# ax.set_yticklabels(['{:3.2f}%'.format(x) for x in np.linspace(0,100,len(vals))])

#Set labels using column #0 (The rotation is important)
ax.set_xticklabels(table.ix[:,0].values,rotation=0)


bars=ax.patches
patterns = ('-', 'x', '\\', '\\\\', '.', '/','//','///')
designs = {}
designs['h_line'] = '-'
designs['squares'] = '+' # A bit random, they look crosses or sometimes lines 
designs['x'] = 'x'
designs['backslash'] = '\\'
designs['2_backlash'] = '\\\\'
designs['backslash'] = '\\'
designs['2_backlash'] = '\\\\'
designs['stars'] = '*' # Kill me please
designs['cheetah'] = 'o'
designs['cheetah2'] = 'O'
designs['sevillana'] = '.'
# And you can combine them
designs['mix']='\/'



#Set hatches and/or colors as desired in bars ...
arr = []
for bar in bars:
	w = bar.get_width()
	bar.set_width(w-0.02)
	bar.set_hatch('/') 
	## Pick the one you like
	#bar.set_color(colors[i]) ## Pick the one you like
	


##Don't forget to update the legend  to reflect the changes
ax.legend(loc='upper center', ncol=nCols) 

#plt.axhspan(ymin, ymax)			
plt.show()