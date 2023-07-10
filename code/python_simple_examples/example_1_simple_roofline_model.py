import matplotlib.pyplot as plt

# Performance data
flops = [1e6, 1e7, 1e8, 1e9]  # FLOPs (floating-point operations) per second
bw = [1e9, 1e10, 1e11, 1e12]  # Memory Bandwidth in bytes per second

# Plotting the Roofline model
plt.figure(figsize=(8, 6))
plt.title("Roofline Performance Model")
plt.xlabel("Arithmetic Intensity (FLOPs/Byte)")
plt.ylabel("Performance (FLOPs/s)")

# Plotting the Roofline boundaries
plt.plot(flops, bw, 'k-', label="Roofline Boundaries")

# Plotting data points
data_points = [(5e7, 5e9), (3e8, 8e9), (8e7, 2e10)]  # Example data points
for point in data_points:
    flops_point, perf_point = point
    plt.scatter(flops_point, perf_point, color='red', label="Data Points")

# Adding annotations to data points
for i, point in enumerate(data_points):
    flops_point, perf_point = point
    plt.annotate(f"Data {i+1}", (flops_point, perf_point),
                 textcoords="offset points", xytext=(-10,10), ha='center')

plt.legend()
plt.grid(True)
plt.show()

