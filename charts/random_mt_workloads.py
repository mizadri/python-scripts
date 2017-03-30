#!/usr/bin/env python
import csv
import sys
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib.markers import *
import pandas as pd
import numpy as np   
import subprocess

def run_bash_command(command):
        process = subprocess.Popen(["bash","-c",command], stdout=subprocess.PIPE)
        return process.communicate()[0]

def pdfcrop(filename):
    run_bash_command("./my_pdfcrop %s" % filename)   

def parseMyExcel(filename):
    ## Build a panda table from CSV or excel
    table=pd.read_excel(filename) ## specify  ('Sheet1', index_col=None, na_values=['NA']) if specific sheet
    ## Get interesting columns only (by name or by number )
    table=table[["Category","HSP.1","HSP.2","ACFS.1","ACFS.2","PropSP.1","PropSP.2","RR.1","RR.2","EQP.1","EQP.2","A-DWRR.1","A-DWRR.2"]]
    schedulers=["HSP","ACFS","Prop-SP","RR","EQP","A-DWRR"]
    ## Get an array of the unique configuration explored
    ## Get column by name plus return data. Get unique fields...

    data={}
    i=1
    for sched in schedulers:
        data[sched]=table.ix[:,[i,i+1]] #.values 
        i=i+2

    return (schedulers,data) ## Data is a dict of panda tables

def generateChart(PointsPlot,labels,markerSpecs,xlabel,ylabel,mode=0,figSize=[9.0,9.0],filename=None,windowTitle=None,legendLocation='best',axes_labelsize=None,xticks=None,yticks=None):

    #plt.rcParams["figure.figsize"]=figSize
    plt.figure(figsize=figSize)
    fig = plt.gcf()
    if windowTitle!=None:
        fig.canvas.set_window_title(windowTitle)

    if axes_labelsize!=None:
        plt.xlabel(xlabel,fontsize=axes_labelsize)
        plt.ylabel(ylabel,fontsize=axes_labelsize)
    else:
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    for serie in labels:#PointsPlot.keys():
        (X,Y)=PointsPlot[serie]

        ## Hack para reconocer el color
        markerSpec=markerSpecs[serie]
        if  len(markerSpec)>1:
            extraArgs=dict(facecolor=markerSpec[1])
        else:
            extraArgs=dict()
        plt.scatter(X, Y, s=75, marker=markerSpec[0], label=serie, **extraArgs) ## B&W (facecolors='none', edgecolors='black',)
        #plt.scatter(X, Y, label=serie, marker=markerSpec[0], markersize=8) # linestyle='dashed')  #markerSpec[0])##'--o')
    
## Leyenda ...
   
    ## Arriba 
#    lgd=plt.legend(loc='center',  bbox_to_anchor=(0.5, 0.95),
#        ncol=6,bbox_transform=plt.gcf().transFigure, 
#        scatterpoints=1,
#        ##frameon=False, Disable blox
#        columnspacing=0.8,handletextpad=0.25) # borderaxespad=0.,)

    #Derecha y dentro
    lgd=plt.legend(loc='center right', #bbox_to_anchor=(0.95, 0.5),
        ncol=1,bbox_transform=plt.gcf().transFigure, 
        scatterpoints=1,
        ##frameon=False, Disable blox
        columnspacing=0.8,handletextpad=0.25) # borderaxespad=0.,)


  ## Para ajustar de verdad los ejes al rango de xs e ys dado (Esto es critico) 
    plt.axis("tight")

## All lines
    plt.grid(True)
## Horizontal lines only
    #plt.gca().yaxis.grid(True)

# Yticks
    if yticks!=None:
        plt.yticks(yticks)

    if xticks!=None:
        plt.xticks(xticks)

## Para que las etiquetas no desaparezcan (cuando el tamanio de la imagen es pequenio)
    #plt.tight_layout()

    plt.draw()
    if filename!=None:
        plt.savefig(filename,
                ## Make sure the legend appears in the figure
                bbox_extra_artists=(lgd,), bbox_inches='tight')


    return 0


#schedulers=["HSP","ACFS","PropSP","RR","EQP","A-DWRR"]

#markersRaw=[['o'],[(4,0,0),'k'],['^'],[(7,2,0)],[(3,0,0),'k'],['o']]
# Formato: Lista de listas
# en cada lista -> pos 0 es el tipo de marker
# TipoDeMarker: caracter o tupla (numsides, style, angle)
#  http://matplotlib.org/1.4.1/api/markers_api.html#module-matplotlib.markers
# pos 1 de la lista es el descriptor de color (acepta caracteres con colores predefinidos)
# , colores HTML, escala de grises (num. entre 0 y 1)
# http://matplotlib.org/1.4.1/api/colors_api.html
markersRaw=[[(4,0,0),'#000000'],['s','#ffff66'],['^','#009900'],[(7,2,0)],['p','#ffffff'],['o','#ff9933']]

#rcParams['text.usetex']= 1

figureSize=[7.75,6.75]


filename = "random_mt_workloads_leviatan.xls" ## sys.argv[1]
pdfname = "random_mt_workloads_leviatan.pdf"
(series,tables)=parseMyExcel(filename)

markerSpecs={}
marker_cnt=0
nr_markers=len(markersRaw)
for serie in series:
    markerSpecs[serie] = markersRaw[marker_cnt%nr_markers]
    marker_cnt = marker_cnt + 1

## Prepare points
plotData={}

for serie in series:    
    ## 2 series
    table=tables[serie]
    ## Preparar tupla de listas (Me quedo con las columnas que quiero de la tabla panda)
    X=table.ix[:,0].values
    Y=table.ix[:,1].values
    plotData[serie]=(X,Y)


## Draw 
yticks_fixed=np.arange(0,1.1,0.1)
xticks_fixed=np.arange(1,3.0,0.2)   
 
fsize=16
rcParams['font.family'] = 'Helvetica'
rcParams['xtick.labelsize'] = fsize
rcParams['ytick.labelsize'] = fsize
rcParams['legend.fontsize'] = fsize
rcParams['grid.linewidth']= 1.0

## Generate chart
generateChart(plotData,series,markerSpecs,"Unfairness","Relative ASP",figSize=figureSize,
    filename=pdfname,windowTitle="workloads",axes_labelsize=fsize,
    xticks=xticks_fixed,yticks=yticks_fixed)

pdfcrop(pdfname)
#Uncomment to display the chart windows
plt.show()
