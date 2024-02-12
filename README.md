
![PiThermal](https://github.com/remsky/ThermalProject/assets/25017870/5a819993-58b1-4b32-b28e-7443c57ada0e)

![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi)
# Raspberry Pi 4 Thermal Camera Project

## Overview
This project involves a Raspberry Pi 4 with an MLX90640 thermal camera, capable of live plotting and displaying thermal images. The script provided is for capturing, processing, and visualizing thermal data in real-time.

## Hardware Requirements
- Raspberry Pi 4
- MLX90640 thermal camera module

## Software Requirements
- Python 3.x
- Libraries: numpy, matplotlib, scipy, adafruit_mlx90640

## Setup
1. **Enable I2C on Raspberry Pi**:
   Use `raspi-config` to enable the I2C interface.

2. **Install Python Libraries**:
   Run `pip install numpy matplotlib scipy adafruit-circuitpython-mlx90640`.

## Running the Script
Execute the script to start capturing and displaying thermal data. The script initializes the camera, sets up the live display, and enters a loop for real-time data processing and visualization.

## Features
- Live thermal image plotting.
- Data interpolation for enhanced clarity.
- Real-time and averaged thermal view modes.
- Frame rate monitoring for performance checks.

## Usage
Run the script in a Python environment. The live thermal feed will display in real-time, and the system will periodically capture and display an averaged thermal image.

---

*Note: Ensure all connections and configurations are correctly set before running the script. Loose wires can cause dropped frames and crashes*
