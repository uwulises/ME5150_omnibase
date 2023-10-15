screen -X -S driver quit; screen -dmS driver bash -c 'cd ~/ME5150_omnibase && source robotica/bin/activate && cd src/serial_control && python3 drive_server.py'
