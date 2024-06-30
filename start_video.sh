#!/bin/bash

screen_name="video"

# Si ya existe un proceso screen llamado "$screen_name", matarlo
if screen -list | grep -q "$screen_name"; then
  screen -S "$screen_name" -X quit
  echo "Matando proceso screen anterior..."
fi

# Iniciar screen y ejecutar el script de Python
screen -dmS "$screen_name" bash -c '
  workon me5150
  echo "Iniciando script de Python..."
  python3 /home/robotica/ME5150_omnibase/server/stream_server/stream_rpi.py
'

# Verificar que se haya creado el screen
if screen -list | grep -q "$screen_name"; then
  echo "Screen $screen_name creado correctamente."
else
  echo "Error al crear screen."
fi