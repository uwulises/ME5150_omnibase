#!/bin/bash
screen -dmS video bash -c '
  workon me5150
  cd ~/ME5150_omnibase/src/control_server
  python3 control_rpi.py
'