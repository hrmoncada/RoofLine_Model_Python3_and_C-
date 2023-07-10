# RoofLine Model
The Roofline performance model is a tool to understand the kernel/hardware limitation.It provides a relatively
simple way for performance estimates based on the computational kernel and hardware characteristics. It provides a
visually-intuitive way for users to identify performance bottlenecks and motivate kernel/code optimization strategies.
The Roofline is a throughput-oriented performance model centered around the interplay between computational
capabilities (e.g. peak GFLOP/s), memory bandwidth (e.g. STREAM GB/s), and data locality (i.e. reuse of data
once it is loaded from memory). Data locality is commonly expressed as arithmetic intensity which is the ratio of
floating-point operations performed to data movement (FLOPs/Bytes).

<p align="center">
<img
  src="https://github.com/hrmoncada/RoofLine_Model_Python3_and_CPP/blob/main/figures/Roofline_0_1.png" width="60%" height="30%"
  alt="Alt text"
  title="Roofline Model"
  style="display: inline-block; margin: 0 auto; max-width: 300px"
  >

# Concepts or Chararcteristics
## Kernel
A kernel is a fundamental component of an software package. A software package can contain multiple kernels
(microkernels). A microkernel can be program of a source code, block section of source code, a layer of source code,etc.
These microkernels deals only with critical activities in software package.

In the case of operating system (OS), kernels handles many fundamental processes at a basic level, communicating
with hardware and managing resources, such as RAM and the CPU. On most systems, the kernel is one of the
programs loaded at the beginning of the boot sequence when a computer starts up. It handles the rest of startup as
well as memory, peripherals, and input/output (I/O) requests from software, translating them into data-processing
instructions for the CPU. The kernel performs a system check and recognizes components, such as the processor,
GPU, and memory.

## proxy applications
In high performance computing (HPC), proxy applications (proxy apps) are small, simplified codes that allow
application developers to share important features of large applications without forcing collaborators to assimilate
large and complex code bases. Proxy apps are often used as models for performance-critical computations, but
proxy apps can do more than just represent algorithms or computational characteristics of apps. They also capture
programming methods and styles that drive requirements for compilers and other elements of the tool chain.

## Load balancing
Load balancing in distributed memory systems refers to the process of distributing a set of tasks over a set of resources
(computing units), with the aim of making their overall processing more efficient and improve performance, typically
by moving work from overloaded resources to underloaded resources. Load balancing techniques can optimize the
response time for each task, avoiding unevenly overloading compute nodes while other compute nodes are left idle.
In short, a load balancer acts as the traffic cop sitting in front of your system manage the requests across all nodes
capable of fulfilling those requests in a manner that maximizes speed and capacity utilization and ensures that no
one node is overworked, which could degrade performance

## Arithmetic Intensity (AI)
Arithmetic Intensity (AI), also referred to as Operational Intensity, Computational Intensity is a measure of (Work)
floating-point operations (FLOPs) performed by a given code (or code section) relative to the (memory traffic)
amount of memory accesses (Bytes) that are required to support those operations. It is most often defined as a
FLOPs per Bytes ratio of floating-point operations performed to data movement (FLOP/Byte). For a given kernel
(code, or code section), we can find a point on the X-axis based on its Arithmetic intensity (AI).

## Python3 and CPP Code
The GPU kernels in the EXESS (Extreme-scale Electronic Structure System) standalone code were profiled on ORNL Crusher HPC to analyze their time and power consumption. An investigation of the multi-GPU workload on GAMESS was conducted to develop a strategy for maximizing performance while considering different power allocations. To measure performance and power on the AMD MI250X GPU, experiments were performed on the OLCF Crusher testbed system. The rocProf tool was utilized to profile the EXESS code during a Hartree-Fock calculation on the w150 input. Additionally, rocProf was employed to gather performance metrics for the most critical GPU kernels in EXESS. The rocm-smi API was used to instrument these GPU kernels and measure their average power consumption and accumulated energy usage.

<p align="center">
<img
  src="https://github.com/hrmoncada/RoofLine_Model_Python3_and_CPP/blob/main/figures/GPU_Crusher_Roofline_Model_LOG.png"
  alt="Alt text"
  title="GAMESS Kernel"
  style="display: inline-block; margin: 0 auto; max-width: 300px"
  >
</p>


