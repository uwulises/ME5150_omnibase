#!/bin/bash
screen -dmS video bash -c '
  workon me5150
  cd ~/ME5150_omnibase/src/stream_server
  echo "Iniciando script de Python: stream_rpi..."
  if python3 stream_rpi.py >> stream_rpi.log 2>&1; then
    echo "El script de Python se está ejecutando."
  else
    echo "Error al iniciar el script de Python."
    echo "Revisa el log en stream_rpi.log"
  fi
'