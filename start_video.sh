screen -X -S video quit
screen -dmS video bash -c '
  cd ~/ME5150_omnibase
  source robotica/bin/activate
  cd src/stream_server
  python3 stream_rpi.py
'