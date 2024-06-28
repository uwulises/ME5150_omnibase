import requests
import json
from webRTC import WebRTCController
from videoShow import VideoShow

class RobotClient:
    def __init__(self, address, port=5000, portVideo=8080):
        self.address = address
        self.port = port
        self.base_url = f"http://{address}:{port}"
        self.connected = False
        self.session = requests.Session()
        self.webRTCUser = WebRTCController(self.address)

    def connect(self):
        if self.connected:
            print("already connected :)")
            return

        url = f"{self.base_url}/connect"
        response = self.session.get(url)
        if response.status_code == 200:
            self.connected = True
            print(response.text)

    def connectWebRTC(self):
        self.webRTCUser.connect()

    def closeWebRTC(self):
        self.webRTCUser.close()
        
    def showVideo(self, process= lambda frame : (frame, None)):
        self.webRTCUser.showVideo(process)
    
    def stopVideo(self):
        self.webRTCUser.stopVideo()

    def get_frame(self):
        return self.webRTCUser.getFrame()
        
    def home(self):
        self.set_joints(q0=self.HOME_Q0, q1=self.HOME_Q1, q2=self.HOME_Q2)


class VideoShow():

    def __init__(self, buffer) -> None:
        self.buffer = buffer
        self.show = self.show = threading.Event()
        self.args = []

    def isRunning(self):
        if self.show:
            return self.show.is_set()

    def showLoop(self):
        # Read until video is completed
        while (self.show.is_set()):
            # Capture frame-by-frame
            frame = self.buffer.getCurrentFrame()
            if frame is not None:
                # Display the resulting frame
                frame, self.args = self.process(frame)
                cv2.imshow('Video', frame)

                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    self.show.clear()
                    break
            # Break the loop
            else: 
                time.sleep(1)
        # When everything done, release the video capture object
        # Closes all the frames
        cv2.destroyAllWindows()

    def start(self, process):
        self.show.set()
        self.process = process
        self.cameraThread = threading.Thread(target=self.showLoop, args=())
        self.cameraThread.start()
    
    def stop(self):
        self.show.clear()
        self.cameraThread.join()
        