#!/bin/bash
# Cleaning
rm data_file.txt out
# Compile
g++ -o out Extract_data_and_build_roofline_model_2.cpp
# Execute
./out >> data_file.txt
# Plotting
python plot_roofline_model_cpp.py

