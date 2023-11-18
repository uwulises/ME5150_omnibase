# ME5150_omnibase

TO DO LIST
<https://www.raspberrypi.com/documentation/computers/os.html#python-on-raspberry-pi>
### OpenCV
Following recommendation of Picamera 2 manual

```sudo apt install -y python3-picamera2```

```sudo apt install -y python3-opencv```

```sudo apt install -y opencv-data```

```sudo apt install screen```

### Python environment

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
