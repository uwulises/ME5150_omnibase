#!/bin/bash
screen -dmS video bash -c '
  cd ~/ME5150_omnibase/src/stream_server
  python3 stream_rpi.py
'