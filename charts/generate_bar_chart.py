#!/usr/bin/env python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import re
import getopt

#import seaborn
#seaborn.set()

# -p p1,p2,p3,..,pn : Patterns for each column ---> '#cccccc:/,...."
# -y y-range: ej: 1:4.20 or 1:4.20:0.1 (Increment is at the end) ----> yticks_fixed=np.arange(0,1.1,0.1)
def usage(help):
	print """Usage: %s -i data_file [options]
---Option List---
-i input-file: CSV input data file.
-d width,height : Dimensions.
-c c1,c2,c3,..,cn : Idx Columns.
-p p1,p2,p3,..,pn : Patterns for each column.
-y y-range: ej: 1:4.20 or 1:4.20:0.1 (Increment is at the end).
-P : enable percentage format on y axis.
-l <ylabel>: set labels for y axis.
-t <tag>: tag that will be appended to the filename of the figure.
-r <offset_x>: Rotate x titles by 90 degrees and apply offset to separate them from the x axis.
-n: no key.
-f <fontspec>
-R <row_selection>
-A: compute average.
-h : help"""% sys.argv[0]

	if not help:
		exit(1)
	else:
		exit(0)           

try:
		opts, args = getopt.getopt(sys.argv[1:], "i:d:c:p:y:kl:t:r:n:f:R:Ah", ["input-file","dimensions","columns","patterns","yrange","percentages","ylabels","tag","roffset","nokey","font","rows","average","help"])
except getopt.GetoptError as err:
	# print help information and exit:
	print str(err) # will print something like "option -a not recognized"
	usage(False)
	sys.exit(2)

	infile = None
	figSize = [7.75,6.75]
	columns = []
	patterns = []
	yrange = None
	percentages = None
	ylabels = []
	tag = None
	roffset = 0
	nokey = False
	font = "Helvetica"
	rows = []
	average = False

	for o, arg in opts:
		if o in ("-i", "--input"):
			infile=arg 
		elif o in ("-d", "--dimensions"):
			figSize = [float(d) for d in arg.split(',')]
		elif o in ("-c", "--columns"):
			columns = arg.split(',')
		elif o in ("-p", "--patterns"):
			for coldesign in arg.split(','):
				patterns.append(coldesign.split(':'))
		elif o in ("-y", "--yrange"):
			infile=yrange
		elif o in ("-P", "--percentages"):
			percentages=arg
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


if len(figSize)!=2:
	print "The dimmension has to be expressed in the following format: 7.75,6.75"
	exit(1)

## MAIN

plt.figure(figsize=figSize)

tb=pd.read_excel("example.xlsx")

# Create the basic plot with pandas default colors and everything ... (Make sure you pick the axes return object)
#http://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.DataFrame.hist.html
ax=tb.plot(kind='bar')
# .hist() te lo hace directamente.

#Set labels using column #0 (The rotation is important)
ax.set_xticklabels(tb.ix[:,0].values,rotation=0)

#Set hatches and/or colors as desired in bars ...

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

nCols = len(tb.columns) - 1
i = 0
colPadding = 0.02
accPadding = colPadding
arr = []
for bar in bars:
	w = bar.get_width()
	bar.set_width(w-0.02)
	bar.set_hatch('/') 
	## Pick the one you like
	#bar.set_color(colors[i]) ## Pick the one you like
	


##Don't forget to update the legend  to reflect the changes
ax.legend(loc='upper center', ncol=3) 
plt.tight_layout(h_pad=10)


#plt.axhspan(ymin, ymax)			
plt.show()
