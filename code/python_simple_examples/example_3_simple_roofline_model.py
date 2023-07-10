'''

This code will generate a basic Roofline performance model plot with three kernel operations: matrix-vector multiplication, matrix-matrix multiplication, and matrix addition. You can modify the performance data (matrix_vector_perf, matrix_matrix_perf, matrix_addition_perf) and memory bandwidth (memory_bandwidth) according to your specific HPC data.



'''

import numpy as np
import matplotlib.pyplot as plt

# Performance data for different kernel operations (in GFLOPS)
mflops_max = 500  # Maximum achievable performance (in GFLOPS)
matrix_vector_perf = 200  # Matrix-vector multiplication performance (in GFLOPS)
matrix_matrix_perf = 300  # Matrix-matrix multiplication performance (in GFLOPS)
matrix_addition_perf = 150  # Matrix addition performance (in GFLOPS)

# Memory bandwidth (in GB/s)
memory_bandwidth = 100

# Roofline plot parameters
x_vals = [1, mflops_max]  # FLOP/s axis
y_vals = [0, mflops_max * memory_bandwidth / 1e3]  # Memory bandwidth axis

# Plot Roofline
plt.plot(x_vals, y_vals, 'r-', label='Roofline')
plt.fill_between(x_vals, y_vals, color='red', alpha=0.1)
plt.xlabel('Arithmetic Intensity (FLOP/Byte)')
plt.ylabel('Performance (GFLOPS)')
plt.title('Roofline Performance Model')

# Plot kernel operations
plt.plot(matrix_vector_perf, matrix_vector_perf * memory_bandwidth / 1e3, 'bo', label='Matrix-Vector')
plt.plot(matrix_matrix_perf, matrix_matrix_perf * memory_bandwidth / 1e3, 'go', label='Matrix-Matrix')
plt.plot(matrix_addition_perf, matrix_addition_perf * memory_bandwidth / 1e3, 'yo', label='Matrix Addition')

# Annotate kernel operations
plt.annotate('Matrix-Vector', (matrix_vector_perf, matrix_vector_perf * memory_bandwidth / 1e3),
             textcoords="offset points", xytext=(-10,10), ha='center')
plt.annotate('Matrix-Matrix', (matrix_matrix_perf, matrix_matrix_perf * memory_bandwidth / 1e3),
             textcoords="offset points", xytext=(-10,10), ha='center')
plt.annotate('Matrix Addition', (matrix_addition_perf, matrix_addition_perf * memory_bandwidth / 1e3),
             textcoords="offset points", xytext=(-10,10), ha='center')

# Set plot limits and legend
plt.xlim(0, mflops_max)
plt.ylim(0, mflops_max * memory_bandwidth / 1e3)
plt.legend(loc='upper left')

# Display the plot
plt.show()

