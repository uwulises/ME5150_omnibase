# ME5150_omnibase

## On your PC

1. Open miniconda console.
2. Pick a folder to save this repo, from now we'll call it ```BASE_PATH```.
3. Clone this repository.
```sh
cd BASE_PATH
git clone https://github.com/uwulises/ME5150_omnibase.git
```
4. Create virtual environment named "omnibase".
```sh
cd client
conda env create -n omnibase
conda activate omnibase
```
5. Install all required packages. This may take a while.
```sh
pip install -r requirements.txt
```

Now you just need to go to VSCode and execute some file, for example: streamClient.py or controlClient.py

## On Raspberry Pi 4
1. Open a Command Prompt, like Windows PowerShell.
2. Connect to Rpi4 via ssh.
```sh
ssh robotica@{ROBOT NAME}.local
```
{ROBOT NAME} can be ```omni1```, ```omni2``` or ```omni3```. If it doesn't work, then use the IP address 192.168.100.XXX (ask for it!) of your mobile base.  
*Ask the password.* 

```sh
ssh robotica@{IP ADDRESS}
```

3. Now that you're on Raspberry Pi, use Ubuntu commands like ```cd``` or ```ls``` to navigate.
4. To **initialize the stream and control** the robot, execute:
```sh
cd ME5150_omnibase
./start_video.sh
./start_control.sh
```
And it's ready.

## Server configuration (rpi4)

1. Open a Command Prompt, like Windows PowerShell.
2. Connect to Rpi4 via ssh.
```sh
ssh robotica@{ROBOT NAME}.local
```
{ROBOT NAME} can be ```omni1```, ```omni2``` or ```omni3```. If it doesn't work, then use the IP address 192.168.100.XXX of the mobile base, use a program like Angry IP Scanner to search. 
*Ask the password.* 

```sh
ssh robotica@{IP ADDRESS}
```

3. Configura la Raspberry Pi. Preguntar por configuracioneees.
```sh
sudo raspi-config
```

4. Update packages. This may take a while.
```sh
sudo apt update
sudo apt upgrade -y 
```

5. Install Git.
```sh
sudo apt install git
```

6. Clone this repository.
```sh
git clone https://github.com/uwulises/ME5150_omnibase.git
```

7. Execute ```install_server.sh``` to install all
```sh
cd ME5150_omnibase/server
chmod +x install_server.sh
./install_server.sh
```
8. It's ready!


---
---
TO DO LIST
<https://www.raspberrypi.com/documentation/computers/os.html#python-on-raspberry-pi>
### OpenCV
Following recommendation of Picamera 2 manual

```sudo apt install -y python3-picamera2```

```sudo apt install -y python3-opencv```

```sudo apt install -y opencv-data```

```sudo apt install screen```

### Python environment
- Install via apt-get install python3-venv
- This should starts with python 3.9.2
```$ cd ME5150_omnibase ```

```$ python -m venv robotica```

### Firmware
- [ ] Edit the cmd_vel(float vx, float vy) function, there's some errors on the rpm output
- [ ] Use the correct kinematic model using cmd_vel
### Image Server
- [x] Change the implementation to aiortc WebRTC
- [x] Improve the framerate output
### Control Server
- [ ] Port all the control moves to cmd_vel standard
- [x] Use requests GET method for call moves

### Xbox generic Control
- [ ] handle the names of the controller when the batterry runs low
- [ ] change the values output of the controller when the batterry runs low
- [ ] Look for another library which works with generic controls

### ImportError when running stream_rpi.py

1. ImportError: libsrtp2.so.1: cannot open shared object file: No such file or directory
<https://linuxhint.com/install-ffmpeg-raspberry-pi/>
```
sudo apt update && sudo apt upgrade -y
sudo apt install ffmpeg -y
```
Ensure that ffmpeg is successfully installed, running:
```
ffmpeg -version
```

2. ImportError: libsrtp2.so.1: cannot open shared object file: No such file or directory
```
sudo apt install libnspr4 libnss3 libsrtp2-1
```
