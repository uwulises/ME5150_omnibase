#!/bin/bash
echo "Installing server"

echo "Updating system..."
sudo apt update
sudo apt upgrade -y

echo "Installing packages..."
sudo apt install build-essential cmake pkg-config python3-pip python3-dev screen -y
sudo pip3 install virtualenv virtualenvwrapper 

echo "Setting up virtual environment..."
cd ~
echo "# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh " >> ~/.bashrc

source ~/.bashrc

echo "Creating virtual environment for server..."
mkvirtualenv me5150 -p python3
echo "Now you are in the virtual environment, to exit type 'deactivate'"

echo "Updating pip..."
pip install --upgrade pip 

echo "Installing server packages..."
cd ME5150_omnibase/server
pip install -r requirements.txt
echo "Packages installed successfully"

echo "Give permission to start scripts..."
cd ~/ME5150_omnibase
chmod +x start_control.sh
chmod +x start_video.sh

echo "Server installed successfully"
