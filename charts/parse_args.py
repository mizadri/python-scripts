import sys
import re
import getopt

def usage(help):
	print "Usage: %s [ -m <metric> | -M <metric-file> | -b ]" % sys.argv[0]

	if not help:
		exit(1)
	else:
		exit(0) 

# if an option is followed by ':' it needs a parameter
try:
	opts, args = getopt.getopt(sys.argv[1:], "hm:M:b", ["input","help","metric","metric-file","bypass","output","verbose","accum","csv"])
except getopt.GetoptError as err:
	# print help information and exit:
	print str(err) # will print something like "option -a not recognized"
	usage(False)
	sys.exit(2)

figSize = [2,2]
expressions=[]    
metricFile=None
bypass=False

for o, arg in opts:
	if o in ("-h", "--help"):
		usage(True)
		sys.exit()
	elif o in ("-m", "--metric"):
		figSize = [float(d) for d in arg.split(',')]
		if len(figSize)!=2:
			print "The dimmension has to be expressed in this format: 'x,y'"
			exit(1)
	elif o in ("-M", "--metric-file"):
		metricFile=True
	elif o in ("-b", "--bypass"):
		bypass=True        	
	else:
		assert False, "unhandled option"

print metricFile