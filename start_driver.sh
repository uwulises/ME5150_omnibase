#!/bin/bash

# Start a screen session named "driver"
screen -S driver

# Change directory to the project
cd ~/ME5150_omnibase

# Source the virtual environment
source robotica/bin/activate

# Change directory to the source folder
cd src/serial_control

# Run the Python script
python3 drive_server.py