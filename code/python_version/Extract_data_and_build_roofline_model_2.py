#!/usr/bin/python3
## The purpose of  the shebang line on the top of the script is to define the location of the interprete

# Import modules
import csv
import re
import os
import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal

#----------------------------------------------------
# Pause
#----------------------------------------------------
def pause():
    program_Pause = raw_input("Press the <ENTER> key to continue...\n")
    plt.cla()   # Clear axis
    plt.clf()   # Clear figure
    plt.close() # Close a figure window
    exit()      # exit program

#---------------------------------------------------------------------------------
# Search patter, similar to LINUX command GREP, return data[], num rows, num cols
#--------------------------------------------------------------------------------
def search_pattern_and_store_in_data(filename, pattern, Data):
    Store = []       # Temporal store lines
    line_count = 0   # Count lines
# Split :  get rid of all the duplicate whitespaces and newline characters, then you can use, # # join() function with string split() function to join with comma and space ", "
    with open(filename, "r") as data:
       for line in data:
           if re.search(pattern, line):
             if pattern=="invocations" :
                line = " ".join(line.split())
             else :
                line = ",".join(line.split())

             line_count += 1
             Store.append(line)

# Separted with the delimiter ',' and store on Data[]
    csv_reader = csv.reader(Store, delimiter=',')
    for row in csv_reader:
        Data.append(row)

# Get the number of rows and columns
    num_rows = len(Data)
    num_cols = len(Data[0])

    return [num_rows, num_cols]

#-------------------------------------------------------------------------------------
# Extract FETCH_SIZE_MOVED, WRITE_SIZE_MOVED, BYTES_MOVED data mmoved from metrics.csv
#------------------------------------------------------------------------------------
def extract_metrics(filename, patterns):
    BYTES_MOVED = []
    FETCH_SIZE_MOVED = []
    WRITE_SIZE_MOVED = []

    for i in range(0,len(patterns)):
       Data = []
       search_pattern_and_store_in_data(filename, patterns[i], Data)

       FETCH_SIZE = 0.0
       WRITE_SIZE = 0.0
       for j in range(0,len(Data)):
          FETCH_SIZE += float(Data[j][18])
          WRITE_SIZE += float(Data[j][19])

       BYTES = 1024*(FETCH_SIZE + WRITE_SIZE)
       BYTES_MOVED.append(BYTES)
       FETCH_SIZE_MOVED.append(FETCH_SIZE)
       WRITE_SIZE_MOVED.append(WRITE_SIZE)

    return FETCH_SIZE_MOVED, WRITE_SIZE_MOVED, BYTES_MOVED
#----------------------------------------------------
# Extrac RUN_TIME data from results.stats.csv
#----------------------------------------------------
def extract_runtime(filename, kernelname):
    RUN_TIME = []

    for i in range(0,len(kernelname)):
       Data = []
# call search_pattern_and_st]ore_in_data subroutine
       search_pattern_and_store_in_data(filename, kernelname[i], Data)
       RUNS = int(Data[0][2])

       RUN_TIME.append(RUNS)

    return RUN_TIME
#----------------------------------------------------
# Get the Average data
#----------------------------------------------------
def extract_FLOPS_Average(filename, kernelname, patterns):
# Store the Average FLOPS
    NFLOPS = []

# For-Loop over filename and kernelname
    for k in range(0,len(filename)):
      Data_Name = 'data_set' + '.' + kernelname[k]  # data set name

# Initialize array size
      num_rows = 20
      num_cols = len(patterns)

      Average = [[0 for x in range(num_cols)] for x in range(num_rows)]

# For-Loop over label patterns (dadd, dfma, dmul)
      for i in range(0,len(patterns)):
         Pattern_Name = kernelname[k] + '.' + patterns[i]
         Data = [] # extract data table

# Call "search_pattern_and_store_in_data"  subroutine
         [num_rows, num_cols] = search_pattern_and_store_in_data(filename[k], patterns[i], Data)

# For-Loop over the rows of Data
         if  patterns[i]=="invocations" :
            for j in range(0,num_rows):
               invocations = Data[j][num_cols-1].split()
               Average[j][i] = int(invocations[0])
         else:
            for j in range(0,num_rows):
               Average[j][i] = float(Data[j][4])

      FLOPS = 0.0
      for line in range(0,num_rows):
        FLOPS += Average[line][0]*(Average[line][1] + 2*Average[line][2] + Average[line][3])

      NFLOPS.append(FLOPS)

    return NFLOPS

#----------------------------------------------------
# Main
#----------------------------------------------------
if __name__ == '__main__':
# Input files
    filename = ['../rerooineperformancemodelplot/exess.w150.0000.ncu-dpflops.out',
                '../rerooineperformancemodelplot/exess.w150.1100.ncu-dpflops.out',
                '../rerooineperformancemodelplot/exess.w150.1110.ncu-dpflops.out']
# Kernels
    kernelname = ["0_0_0_0","1_1_0_0","1_1_1_0"]

# Patters
    patterns = ["invocations","dadd", "dfma", "dmul"]

# Extract average number of flops by kernel
    NFLOPS = extract_FLOPS_Average(filename, kernelname, patterns)

# Include kernel "1_0_0_0" NFLOPS
    kernelname = ["0_0_0_0","1_0_0_0","1_1_0_0","1_1_1_0"]
    NFLOPS.insert(1,2812154194667)
#-------------------------------------------------------------------------
# Extract the data move from "metrics"
    kernelname = ["0_0_0_0","1_0_0_0","1_1_0_0","1_1_1_0"]

    filename = "../rerooineperformancemodelplot/metrics.csv"
    FETCH_SIZE_MOVED,  WRITE_SIZE_MOVED, BYTES_MOVED =  extract_metrics(filename, kernelname)
#-------------------------------------------------------------------------
#  Extract the execution time from "resulta.stat"
    filename = "../rerooineperformancemodelplot/results.stats.csv"
    RUN_TIME = extract_runtime(filename, kernelname)
#-------------------------------------------------------------------------
    print("| kernelname | Num of FLOPS |FETCH_SIZE  |  WRITE_SIZE |  1024*(FETCH_SIZE + WRITE_SIZE) | RUN TIME |")
    for i in range(0,len(BYTES_MOVED)):
       print("%s :  %10.1f  %f  %f       %10.1f            %10.1f"%(kernelname[i], NFLOPS[i], FETCH_SIZE_MOVED[i], WRITE_SIZE_MOVED[i], BYTES_MOVED[i], RUN_TIME[i]))

#-------------------------------------------------------------------------
# Plotting - The Roofline Model
# x-axis - Computational Intensity or Aritmetic_Intensity [FLOP/Bytes]
# y-axis - Attainable_Peak_performance [GFLOPS/s] = [FLOPSx10^9/s]
# m slope - Bandwidth [GFLOPS/s]/FLOP/Bytes]] = [GBytes/s]
# y =  mx + b, where b = 0,
# Attainable_Peak_performance =  Bandwidth x Computational Intensity + b
# b = 0, Since Attainable Peak Performance is equal zero when Computational Intensity
#        is equal to zero
# Knee point : Interception betwen the Computational Intensity and Bandwidth
# y = mx => x = y/m
# Attainable_Peak_performance =  Bandwidth x Computational Intensity
# Computational Intensity = Bandwidth / Attainable_Peak_performance
#-------------------------------------------------------------------------
#Giga FLOP 10^9
GIGA =  10**9

# Tera FLOP 10^12;
TERA = 10**12

# Nano seconds 10^-9
ns = 10**(-9)

# P_max : Peak Performance [TFLOP/s]
peak_limited_by_execution = 26.5*TERA
print("\nP_peak : Peak Performance = %.2E\n"%(float(peak_limited_by_execution)))

# Memory Bandwidth (I.b_s) [TBytes/s]
peak_limited_by_data_transfer = 1.6*TERA
print("Bandwidth = %.2E\n"%(float(peak_limited_by_data_transfer)))

# x-axis Aritmetic Intensity [FLOP/Bytes]= [NFLOPS]/[BYTES_MOVED]
Aritmetic_Intensity = [i / j for i, j in zip(NFLOPS, BYTES_MOVED)]
print("Aritmetic_Intensity = ",Aritmetic_Intensity)

# y-axis Attainable Peak Performance [TFLOP/s] = [NFLOPS]/ [RUN_TIME x ns]
RUN_TIME_ns  = [i * ns for i in RUN_TIME]
Attainable_Peak_performance = [i / j for i, j in zip(NFLOPS, RUN_TIME_ns)]
print("\nAttainable Peak Performance = ",Attainable_Peak_performance)

# Knee point (x, y) = (x_AI, P_max)
# Peak_performance =  Bandwidth x Arithmetic Intensity
# Aritmetic_Intensity = Peak_performance / Bandwidth = [TFLOP/s]/[TBytes/s] = [FLOP/Bytes]
x_AI = peak_limited_by_execution/peak_limited_by_data_transfer
print("\nknee point (x_AI, P_peak) = (%5.2f, %.2E)\n"%(float(x_AI), float(peak_limited_by_execution)))

#-------------------------------------------------------------------------
# Plotting
#-------------------------------------------------------------------------
colors = np.array(['red', 'blue', 'green','magenta'])
markers = np.array(['o', 's', 'd', 'v'])

#-------------------------------------------------------------------------
# Regular Plotting
#-------------------------------------------------------------------------
fig1 = plt.figure(1)

plt.plot(x_AI, peak_limited_by_execution, 'ko', markersize=12)
plt.text(-2, peak_limited_by_execution*1.03,'(x_AI, P_peak)' ,rotation=0, fontsize=20)

# Upper bound, horizontal line
plt.hlines(peak_limited_by_execution, xmin=x_AI, xmax=300, linewidth=2, color='r', linestyle='-')

plt.text(100, peak_limited_by_execution*1.03,'Peak performance (TFLOP/s)',rotation=0, fontsize=20)

# Vertical and horizontal line, Machine Balance (Knee point)
plt.vlines(x_AI, 0, peak_limited_by_execution, colors ="r", linestyles ="dotted")
plt.hlines(peak_limited_by_execution, xmin=0, xmax=x_AI, color='r', linestyle="dotted")

# Slope Memory Bandwidth - y = mx + b
x = np.linspace(0, x_AI,10)
y = peak_limited_by_data_transfer*x

plt.plot(x, y, '-r')
plt.text(-2.5, peak_limited_by_data_transfer*7,'Bandwidth (TByte/s)',rotation=85, fontsize=20)

# Plot over the Kernel points
for i in range(len(colors)):
    #plt.scatter(Aritmetic_Intensity[i], Attainable_Peak_performance[i], marker=markers[i], s = 100, c=colors[i],label=kernelname[i])
    plt.plot(Aritmetic_Intensity[i], Attainable_Peak_performance[i], marker=markers[i], linestyle='', markersize=12, color=colors[i],label=kernelname[i])

plt.xlim(-1, 300)
plt.ylim(-1, 1.1*peak_limited_by_execution)

plt.xlabel('Arithmetic Intensity [flop/byte]', fontsize=18)
plt.ylabel('Attainable Performance [TFLOPS]', fontsize=18)
plt.title('MI250X GPU on Crusher\n'+ '(Peak Performance 26.5  [TFLOP/s], Bandwidth 1.6 [TByte/s])', fontsize=20)
plt.grid(color='r', linestyle="dotted", linewidth=.5)
plt.legend(loc=4, bbox_to_anchor=(0.95,0.5), title='Kernels', title_fontsize=20, fontsize=20)


# Additional information on the plot
plt.axhline(peak_limited_by_execution, color="green", linestyle="--", label="Peak Performance")
plt.plot(x, y, color="orange", linestyle="--", label="Bandwidth")
plt.legend()
#-------------------------------------------------------------------------
# Log-Log Plotting
#-------------------------------------------------------------------------
fig2 = plt.figure(2)

plt.plot(x_AI, peak_limited_by_execution, 'ko', markersize=12)
plt.text(-2, peak_limited_by_execution*1.03,'(x_AI, P_peak)' ,rotation=0, fontsize=20)

# Upper bound, horizontal line
plt.hlines(peak_limited_by_execution, xmin=x_AI, xmax=500, linewidth=2, color='r', linestyle='-')

plt.text(20, peak_limited_by_execution*1.03,'Peak Performance (FLOP/s)',rotation=0, fontsize=20)

# Vertical and horizontal line, Machine Balance (Knee point)
plt.vlines(x_AI, 0, peak_limited_by_execution, colors ="r", linestyles ="dotted")
plt.hlines(peak_limited_by_execution, xmin=0, xmax=x_AI, color='r', linestyle="dotted")

# Slope Memory Bandwidth - y = mx + b
x = np.linspace(0, x_AI,10)
y = peak_limited_by_data_transfer*x
plt.plot(x, y, '-r')

plt.text(3.2, peak_limited_by_data_transfer*4,'Bandwidth (TByte/s)',rotation=43, fontsize=20)

# Plot over the Kernel points
for i in range(len(colors)):
    plt.loglog(Aritmetic_Intensity[i], Attainable_Peak_performance[i], marker=markers[i], linestyle='', markersize=12, color=colors[i],label=kernelname[i])

plt.xlim(-1, 500)
plt.ylim(-1, 1.2*peak_limited_by_execution)

plt.xlabel('Arithmetic Intensity [flop/byte]', fontsize=18)
plt.ylabel('Attainable Performance [FLOP/s]', fontsize=18)
plt.title('MI250X GPU on Crusher\n'+ '(Peak Performance 26.5  [TFLOP/s], Bandwidth 1.6 [TByte/s])', fontsize=20)
#plt.grid(color='r', linestyle="dotted", linewidth=.5)
plt.grid(True, which="both", color='r', linestyle="dotted", linewidth=.5,)
plt.yticks([10**12,  10**13, 10**14])
#plt.yticks(np.arange(10**12, 10**14, 10**9))

plt.legend(loc=4, bbox_to_anchor=(0.99,0.715), title='Kernels', title_fontsize=20, fontsize=20)

# Additional information on the plot
plt.axhline(peak_limited_by_execution, color="green", linestyle="--", label="Peak Performance")
plt.plot(x, y, color="orange", linestyle="--", label="Bandwidth")
plt.legend()
#-------------------------------------------------------------------------
# plots are save on figures/
plt.show()
fig1.savefig('figures/GPU_Crusher_Roofline_Model.pdf')
fig2.savefig('figures/GPU_Crusher_Roofline_Model_LOG.pdf')




#

