#!/usr/bin/env python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.markers import *
import matplotlib.font_manager as fm
import sys
import re
import getopt
import os.path

# Problems detecting fonts
# Edit file: subl ~/anaconda2/lib/python2.7/site-packages/matplotlib/mpl-data/matplotlibrc
# Remove font cache(reloads config file when started): sudo rm -rf ~/.cache/matplotlib/


# -p p1,p2,p3,..,pn : Patterns for each column ---> '#cccccc:/,...."
# -y y-range: ej: 1:4.20 or 1:4.20:0.1 (Increment is at the end) ----> yticks_fixed=np.arange(0,1.1,0.1)
def usage(help):
	print """Usage: %s -i data_file [options]
---Option List---
-i <input-file>: Input data file(excel or csv).
-o <output>: Output file data file(excel or csv).
-s <sheet-name>: Excel sheet to obtain the data from.
-d <width,height>: Dimensions.
-c <c1,c2,..,cn>: Column's names to remove.
-p <p1,p2,..,pn> : Patterns for each column( #ffffff:/,#aaaaaa:\,... )
-y <start,end[,step]>: ej: 1:4.20 or 1:4.20:0.1 (Increment is at the end).
-P : Enable percentage format on y axis.
-l <ylabel>: set label for y axis.
-t <tag>: Tag that will be appended to the filename of the figure.
-r <roffset_x>: Rotate x titles by 90 degrees and apply offset to separate them from the x axis.
-n : no key.
-f <fontspec>
-F <fontsize>
-R <row_selection>
-A : compute average.
-h : help"""% sys.argv[0]

	if not help:
		exit(1)
	else:
		exit(0)

try:
	opts, args = getopt.getopt(sys.argv[1:], "i:o:s:d:c:p:y:Pl:t:r:nf:F:R:Ah",
											 ["infile","outfile","sheet","dimensions","columns","patterns"
											 ,"yrange","percentages","ylabel","tag","roffset"
											 ,"nokey","font","fontsize","rows","average","help"])
except getopt.GetoptError as err:
	# print help information and exit:
	print str(err) # will print something like "option -a not recognized"
	usage(False)
	sys.exit(2)


infile = "example.xlsx"
outfile = None
sheet = None
figSize = [10.75,6.75]
columns = None
patterns = []
yrange = None
percentages = False
ylabel = []
tag = None
roffset = 0
nokey = False
font = "sans-serif"
fsize=12
rows = []
average = False

ystart = None
yend = None
ystep = None

for o, arg in opts:
	if o in ("-i", "--infile"):
		infile=arg 
		assert os.path.isfile(infilen), "Specify an existing input file: -i example.xlsx"
	elif o in ("-o", "--output"):
		outfile=arg
	elif o in ("-s", "--sheet"):
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
		yrange = np.arange(ystart,yend,ystep)
	elif o in ("-P", "--percentages"):
		percentages=True
	elif o in ("-l", "--ylabel"):
		ylabel=arg
	elif o in ("-t", "--tag"):
		tag=arg
	elif o in ("-r", "--roffset"):
		roffset=float(arg)
	elif o in ("-n", "--nokey"):
		nokey=True
	elif o in ("-f", "--font"):
		font=arg
	elif o in ("-F", "--fontsize"):
		fsize=int(arg)
	elif o in ("-R", "--rows"):
		rows=arg
	elif o in ("-A", "--average"):
		average=True
	elif o in ("-h", "--help"):
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

if average:
	means = table.mean()
	workload_field = table.columns[0]
	means[workload_field] = "Average"
	table = table.append(means, ignore_index=True)


nCols = len(table.columns) - 1
nRows = len(table)

# Filter columbs by name
if columns:
	table.drop(columns,axis=1,inplace=True)
	nCols -= len(columns)

# for presentation use:
# plt.style.use('presentation')
# for papers use:
# plt.style.use('grayscale')


# Create the plot
ax=table.plot(kind='bar',figsize=figSize,  yticks=yrange, edgecolor='black',)

if ylabel:
	plt.ylabel(ylabel)


plt.title('Unfairness Factor')

#To install a new font
# 1. Copy .ttf to matplotlib instalation(mine is inside anaconda):
	# cp ~/Downloads/Helvetica.ttf ~/anaconda2/lib/python2.7/site-packages/matplotlib/mpl-data/fonts/ttf/
# 2. Set configuration in matplotlibrc file (two last steps set the new font to default):
	#   uncomment and set:
	# pdf.fonttype       : 42
	# ps.fonttype       : 42
	# font.family         : sans-serif
	# font.sans-serif     : Helvetica, DejaVu Sans, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Arial, Avant Garde, sans-serif
# 3. Wipe matplotlib cache to reload it the next time it executes
	# sudo rm -rf ~/.cache/matplotlib/

plt.rcParams['font.family'] = "Helvetica"
plt.rcParams['xtick.labelsize'] = fsize
plt.rcParams['ytick.labelsize'] = fsize
plt.rcParams['legend.fontsize'] = fsize
plt.rcParams['grid.linewidth']= 1.0



# vals = ax.get_yticks()
# ax.set_yticklabels(['{:3.2f}%'.format(x) for x in np.linspace(0,100,len(vals))])

#Set labels using column #0 (The rotation is important)
ax.set_xticklabels(table.ix[:,0].values,rotation=0)


#nice_patterns = ('/', '\\', '.', '-', 'x', '\\\\' ,'//','///')
nice_patterns = ('/', '-', '\\')
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
bars=ax.patches
count = 0
i = 0
# Caution: bars are not ordered as you see on the figure. You get the first n columns, then the 2nd n columns..
for bar in bars:

	w = bar.get_width()
	bar.set_width(w-0.02)
	if patterns:
		bar.set_hatch(patterns[i%nCols][1]) 
		## Pick the one you like
		bar.set_color(patterns[i%nCols][0]) ## Pick the one you like
	else:
		bar.set_hatch(nice_patterns[i%nCols])
	
	count += 1

	if count == nRows:
		count = 0
		i += 1

##Don't forget to update the legend  to reflect the changes
ax.legend(loc='upper right', ncol=nCols) 


if not outfile:
	outfile = infile.split(".")[0] + ".pdf"

if tag:
	outfile = "%s.%s.pdf"%(outfile.split(".")[0],tag)


plt.savefig(outfile, bbox_inches='tight')

plt.show()

plt.close()

