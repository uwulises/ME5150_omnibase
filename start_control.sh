#!/bin/bash
screen -dmS video bash -c '
  workon me5150
  cd ~/ME5150_omnibase/src/control_server
  if python3 control_rpi.py >> control_rpi.log 2>&1; then
    echo "El script de Python se está ejecutando."
  else
    echo "Error al iniciar el script de Python."
    echo "Revisa el log en control_rpi.log"
  fi
  
'