#!/usr/bin/python3

# Import modules
import matplotlib.pyplot as plt
import numpy as np


filename = "data_file.txt"
delimiter = ","

# Initialize empty arrays
kernels = []
num_flops = []
fetch_size = []
write_size = []
fetch_write_sum = []
run_time = []
arithmetic_intensity = []
attainable_peak_performance = []

# Read the file
with open(filename, "r") as file:
    next(file)  # skip first line
    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace
        if line:  # Skip empty lines
            data = line.split(delimiter)
            if len(data) == 8:  # 5 rows with length = 8
                # Assuming the line contains kernel data
                kernels.append(data[0].strip())
                num_flops.append(float(data[1].strip()))
                fetch_size.append(float(data[2].strip()))
                write_size.append(float(data[3].strip()))
                fetch_write_sum.append(float(data[4].strip()))
                run_time.append(float(data[5].strip()))
                arithmetic_intensity.append(float(data[6].strip()))
                attainable_peak_performance.append(float(data[7].strip()))
            elif len(data) == 2:   # 2 rows with length = 2 ,  1 rows with length = 3
                # Assuming the line contains additional information
                if data[0].strip() == "Peak_Performance(P_peak)":
                    peak_performance = float(data[1].strip())
                elif data[0].strip() == "Bandwidth(BW)":
                    bandwidth = float(data[1].strip())
                elif data[0].strip() == "Knee_Point_x":
                    knee_point_x = float(data[1].strip())
                elif data[0].strip() == "Knee_Point_y":
                    knee_point_y = float(data[1].strip())

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
# Plotting
#-------------------------------------------------------------------------
colors = np.array(['red', 'blue', 'green','magenta'])
markers = np.array(['o', 's', 'd', 'v'])
#-------------------------------------------------------------------------
# Regular Plotting
#-------------------------------------------------------------------------
fig1 = plt.figure(1)

plt.plot(knee_point_x, knee_point_y, 'ko', markersize=12)
plt.text(-2, knee_point_y*1.03,'(x_AI, P_peak)' ,rotation=0, fontsize=20)

# Upper bound, horizontal line
plt.hlines(knee_point_y, xmin= knee_point_x, xmax=300, linewidth=2, color='r', linestyle='-')

plt.text(100, knee_point_y*1.03,'Peak performance (TFLOP/s)',rotation=0, fontsize=20)

# Vertical and horizontal line, Machine Balance (Knee point)
plt.vlines(knee_point_x, 0, knee_point_y, colors ="r", linestyles ="dotted")
plt.hlines(knee_point_y, xmin=0, xmax= knee_point_x, color='r', linestyle="dotted")

# Slope Memory Bandwidth - y = mx + b
x = np.linspace(0, knee_point_x,10)
y = bandwidth * x
#plt.axline((0, 4), slope=3., color='C0', label='by slope')
plt.plot(x, y, '-r')
plt.text(-2.5, bandwidth * 7,'Bandwidth (TByte/s)',rotation=85, fontsize=20)

# Plot over the Kernel points
for i in range(len(colors)):
    #plt.scatter(Aritmetic_Intensity[i], Attainable_Peak_performance[i], marker=markers[i], s = 100, c=colors[i],label=kernelname[i])
    plt.plot(arithmetic_intensity[i], attainable_peak_performance[i], marker=markers[i], linestyle='', markersize=12, color=colors[i],label=kernels[i])

plt.xlim(-1, 300)
plt.ylim(-1, 1.1*knee_point_y)

plt.xlabel('Arithmetic Intensity [flop/byte]', fontsize=18)
plt.ylabel('Attainable Performance [TFLOPS]', fontsize=18)
plt.title('MI250X GPU on Crusher\n'+ '(Peak Performance 26.5  [TFLOP/s], Bandwidth 1.6 [TByte/s])', fontsize=20)
plt.grid(color='r', linestyle="dotted", linewidth=.5)
plt.legend(loc=4, bbox_to_anchor=(0.95,0.5), title='Kernels', title_fontsize=20, fontsize=20)

# Additional information on the plot
plt.axhline(peak_performance,color="green", linestyle="--", label="Peak Performance")
plt.plot(x, y, color="orange", linestyle="--", label="Bandwidth")
plt.legend()
#-------------------------------------------------------------------------
# Log-Log Plotting
#-------------------------------------------------------------------------
fig2 = plt.figure(2)

plt.plot(knee_point_x, knee_point_y, 'ko', markersize=12)
plt.text(-2, knee_point_y*1.03,'(x_AI, P_peak)' ,rotation=0, fontsize=20)
#plt.text(x_AI-5,-1000,'x_AI' ,rotation=0, fontsize=20)

# Upper bound, horizontal line
plt.hlines(knee_point_y, xmin=knee_point_x, xmax=500, linewidth=2, color='r', linestyle='-')

plt.text(20, knee_point_y*1.03,'Peak Performance (FLOP/s)',rotation=0, fontsize=20)

# Vertical and horizontal line, Machine Balance (Knee point)
plt.vlines(knee_point_x, 0, knee_point_y, colors ="r", linestyles ="dotted")
plt.hlines(knee_point_y, xmin=0, xmax=knee_point_x, color='r', linestyle="dotted")

# Slope Memory Bandwidth - y = mx + b
x = np.linspace(0, knee_point_x,10)
y = bandwidth * x
#plt.axline((0, 4), slope=3., color='C0', label='by slope')
plt.plot(x, y, '-r')

plt.text(3.2, bandwidth * 4,'Bandwidth (TByte/s)',rotation=43, fontsize=20)

# Plot over the Kernel points
for i in range(len(colors)):
    plt.loglog(arithmetic_intensity[i], attainable_peak_performance[i], marker=markers[i], linestyle='', markersize=12, color=colors[i],label=kernels[i])

plt.xlim(-1, 500)
plt.ylim(-1, 1.2*knee_point_y)

# after plotting the data, format the labels
#current_values = plt.gca().get_yticks()
#plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values]) # No decimal places

plt.xlabel('Arithmetic Intensity [flop/byte]', fontsize=18)
plt.ylabel('Attainable Performance [FLOP/s]', fontsize=18)
plt.title('MI250X GPU on Crusher\n'+ '(Peak Performance 26.5  [TFLOP/s], Bandwidth 1.6 [TByte/s])', fontsize=20)
#plt.grid(color='r', linestyle="dotted", linewidth=.5)
plt.grid(True, which="both", color='r', linestyle="dotted", linewidth=.5,)
plt.yticks([10**12,  10**13, 10**14])
#plt.yticks(np.arange(10**12, 10**14, 10**9))

plt.legend(loc=4, bbox_to_anchor=(0.99,0.715), title='Kernels', title_fontsize=20, fontsize=20)

# Additional information on the plot
plt.axhline(peak_performance,color="green", linestyle="--", label="Peak Performance")
plt.plot(x, y, color="orange", linestyle="--", label="Bandwidth")
plt.legend()
#-------------------------------------------------------------------------
# plots are save on figures/
plt.show()
fig1.savefig('figures/GPU_Crusher_Roofline_Model.pdf')
fig2.savefig('figures/GPU_Crusher_Roofline_Model_LOG.pdf')


