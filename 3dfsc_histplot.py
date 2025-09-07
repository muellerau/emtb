#!/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import argparse
from math import sqrt

def StandardDeviation(input):
    input_num = [float(c) for c in input]
    mean = sum(input_num) / len(input_num)
    diff = [a - mean for a in input_num]
    sq_diff = [b ** 2 for b in diff]
    ssd = sum(sq_diff)
    variance = ssd / (len(input_num) - 1)
    sd = sqrt(variance)
    return sd


def Mean(input):
    input_num = [float(c) for c in input]
    mean = sum(input_num) / len(input_num)
    return mean


def HistogramCreation(histogram_sampling, ResEM3DFSCOutglobalFSC, outname, apix, cutoff, sphericity, global_resolution, filetype, histbins, ylimits, xlimits, rbw):
        
        stddev = []
        mean = []
        for i in histogram_sampling:
                stddev.append(StandardDeviation(i))
                mean.append(Mean(i))
        
        stdplusone = [mean[a] + stddev[a] for a in range(len(mean))]
        stdminusone = [mean[a] - stddev[a] for a in range(len(mean))]
        
        ## Open Global FSC
        
        #a = open("Results_" + ThreeDFSC + "/ResEM" + ThreeDFSC + "OutglobalFSC.csv","r")
        a = open(ResEM3DFSCOutglobalFSC,"r")
        b = a.readlines()
        #b.pop(0)
        b.pop(-1)
        
        globalspatialfrequency = []
        globalfsc = []
        
        for i in b:
                k = (i.strip()).split(",")
                globalspatialfrequency.append(float(k[0])/apix)
                globalfsc.append(float(k[2]))
        #print (len(globalspatialfrequency))
        if xlimits:
            maxrange = xlimits[1]
            minrange = xlimits[0]
        else:
            maxrange = max(globalspatialfrequency)
            minrange = min(globalspatialfrequency)
        
        ## Histogram
        
        histogramlist = []
        
        for i in range(len(histogram_sampling[0])):
                for j in range(len(histogram_sampling)):
                        if float(histogram_sampling[j][i]) < cutoff: ##Changed to 0.5
                                break
                        else:
                                output = globalspatialfrequency[j]
                histogramlist.append(float(output))
        
        #HistogramRawOutput = open("Results_" + ThreeDFSC + "/histogram_values.lst","w")
        #for i in histogramlist:
        #        HistogramRawOutput.write(str(i) + "\n")
        #HistogramRawOutput.close()
        
        ## Plotting

        plt.title("Histogram and Directional FSC Plot for %s \n Sphericity = %0.3f out of 1. Global resolution = %0.2f $\AA$.\n \n \n \n" % ('3DFSC', sphericity, global_resolution))
        ax1 = plt.subplot(111)
        ax1.set_xlim([minrange,maxrange])
        if ylimits:
            ax1.set_ylim([ylimits[0], ylimits[1]])
        n, bins, patches = plt.hist(histogramlist, bins=histbins, range=(minrange,maxrange), rwidth=rbw)
        ax1.set_ylabel("Percentage of Per Angle FSC (%)", color="#0343df")
        for tl in ax1.get_yticklabels():
                tl.set_color("#0343df")

        ax2 = ax1.twinx()
        ax2.set_ylim([0,1])
        ax2.set_xlim([minrange,maxrange])
        ax2.plot(globalspatialfrequency, globalfsc, linewidth=1, color="#e50000")
        ax2.plot(globalspatialfrequency, stdplusone, linewidth=1, linestyle="--", color="#15b01a")
        ax2.plot(globalspatialfrequency, stdminusone, linewidth=1, linestyle="--", color="#15b01a")
        ax2.plot((minrange,maxrange), (cutoff, cutoff), linestyle="--", color="#929591")
        ax2.set_ylabel("Directional Fourier Shell Correlation", color='#e50000')
        for tl in ax2.get_yticklabels():
                tl.set_color("r")
                
        blue_patch = mpatches.Patch(color="#0343df", label="Histogram of Directional FSC")
        red_solid_line = mlines.Line2D([], [], color="#e50000", linewidth=3, label="Global FSC")
        green_dotted_line = mlines.Line2D([], [], color="#15b01a", linestyle="--", label="$\pm$1 S.D. from Mean of Directional FSC")
        #box = ax1.get_position()
        #ax1.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
        #ax2.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
        ax1.legend(handles=[blue_patch, green_dotted_line, red_solid_line],loc='center', bbox_to_anchor=(0.5, 1.1), ncol=2)
        xlabel = ax1.set_xlabel("Spatial Frequency ($\AA^{-1}$)")

        #plt.show()
        plt.savefig(outname + "." + filetype, bbox_extra_artists=[xlabel], bbox_inches="tight")
        #plt.savefig(outname + ".png", bbox_extra_artists=[xlabel], bbox_inches="tight")
        
        #Flush out plots
        plt.clf()
        plt.cla()
        plt.close()
        
        ## Return useful values for ChimeraOutputCreate
        # Max Res, Min Res, global spatial frequency list, global FSC list
        return(1/float(max(histogramlist)),1/float(min(histogramlist)),globalspatialfrequency,globalfsc)


def myFxn(input_file, output_file):
    # Example logic: just print the arguments
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Plot ThreeDFSC graphs properly.")
    parser.add_argument('-i', '--histFile', required=True, help='File with raw histogram values (typically histogram_raw.csv)')
    parser.add_argument('-r', '--resemFile', required=True, help='File with global FSC values (typically ResEM3DFSCOutglobalFSC.csv)')
    parser.add_argument('-f', '--fmt', default='png', choices=['png', 'jpg', 'pdf', 'svg'], help='(optional, default = png) Plot file format (png, pdf, svg, jpg)')
    parser.add_argument('--sphericity', type=float, default=0, help='(optional, default = 0) Sphericity value')
    parser.add_argument('-p', '--apix', type=float, required=True, help='Pixel size')
    parser.add_argument('--FSCcutoff', type=float, default=0.143, help='(optional, default = 0.143) FSC cutoff')
    parser.add_argument('--relbarwidth', type=float, default=1, help='(optional, default = 1) Relative width of histogram bars')
    parser.add_argument('--globalfsc', type=float, default=99, help='(optional, default = 99) Global FSC resolution at threshold')
    parser.add_argument('--ylim', nargs=2, type=float, metavar=('YMIN', 'YMAX'), help='(optional, default = autoscale)Y-axis limits for histogram')
    parser.add_argument('--xlim', nargs=2, type=float, metavar=('XMIN', 'XMAX'), help='(optional, default = values from global FSC file) X-axis limits of plot')
    parser.add_argument('--bins', type=int, default=10, help='(optional, default = 10) Number of bins for histogram')
    parser.add_argument('-o', '--out', required=True, help='Name of the output file (include any path, but excluding file extension)')
    
    args = parser.parse_args()
    
    histsamp_data = np.loadtxt(args.histFile, delimiter=',')
    
    HistogramCreation(histsamp_data, args.resemFile, args.out, args.apix, args.FSCcutoff, args.sphericity, args.globalfsc, args.fmt, args.bins, args.ylim, args.xlim, args.relbarwidth)


if __name__ == "__main__":
    main()
