# First, quit the existing screen session named "driver" (if it exists)
screen -X -S driver quit

# Then, create a new detached screen session named "driver"
# and execute the desired commands within it
screen -dmS driver bash -c '
  cd ~/ME5150_omnibase
  source robotica/bin/activate
  cd src/serial_control
  python3 drive_server.py
'
