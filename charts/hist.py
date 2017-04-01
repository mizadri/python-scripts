#!/usr/bin/env python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn

#seaborn.set()


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
