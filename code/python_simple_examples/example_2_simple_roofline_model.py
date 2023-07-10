'''
In this code, we have a set of performance data points represented by flops (FLOPs) and bandwidth (memory bandwidth). The Roofline model is plotted based on the theoretical peak performance (peak_performance) and the maximum memory bandwidth (max_bandwidth). The code uses Matplotlib to create the plot, with the Roofline limits displayed as dashed lines and the data points shown as blue circles.

You can customize the values in the flops and bandwidth lists to represent your specific HPC data, and adjust the peak_performance and max_bandwidth parameters accordingly.

Note: The code provided is a simplified example to demonstrate the concept of the Roofline performance model. In practice, more complex calculations and considerations may be necessary to accurately represent the performance characteristics of a specific system or application.
'''


import matplotlib.pyplot as plt
import numpy as np

# Performance data (FLOPs and memory bandwidth)
flops = [1e9, 1e10, 1e11, 1e12]  # FLOPs (e.g., theoretical peak performance)
bandwidth = [10e9, 50e9, 100e9, 200e9]  # Memory bandwidth (e.g., GB/s)

# Roofline model parameters
peak_performance = 1e12  # Theoretical peak performance (FLOPs)
max_bandwidth = 200e9  # Maximum memory bandwidth (GB/s)

# Plotting the Roofline model
plt.figure(figsize=(8, 6))
plt.title("Roofline Performance Model")
plt.xlabel("Arithmetic Intensity (FLOPs/Byte)")
plt.ylabel("Performance (FLOPs/s)")

# Plotting the Roofline limits
plt.plot([0, peak_performance / max_bandwidth], [0, peak_performance], 'k--', label="Roofline Limit")
plt.plot([0, 1], [0, peak_performance], 'r--', label="Attainable Performance")

# Plotting the data points
for i in range(len(flops)):
    intensity = flops[i] / bandwidth[i]
    plt.plot(intensity, flops[i], 'bo', label="Data Point {}".format(i + 1))

plt.legend()
plt.grid(True)
plt.show()

