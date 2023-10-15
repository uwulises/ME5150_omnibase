# First, quit the existing screen session named "video" (if it exists)
screen -X -S video quit

# Then, create a new detached screen session named "video"
# and execute the desired commands within it
screen -dmS video bash -c '
  cd ~/ME5150_omnibase
  source robotica/bin/activate
  cd src/stream_server
  python3 stream_rpi.py
'