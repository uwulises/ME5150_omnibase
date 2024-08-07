import asyncio
import cv2
import threading
import time


class VideoBuffer():
    def __init__(self, cond) -> None:
        self.started = False
        self.frame = None
        self.initCond = cond

    async def addTrack(self, track):
        self.track = track
    
    def isRunning(self):

        return self.started 

    async def start(self):
        self.started = True
        self.startTask = asyncio.current_task()
        self.frame = await self.track.recv()
        with self.initCond:
            self.initCond.notify()
        while (self.started):
            self.frame = await self.track.recv()
    
    async def stop(self):
        self.started = False
        await asyncio.wait_for(self.startTask, timeout=10)
    
    def getCurrentFrame(self):
        if self.frame is None:
            return None
        return self.frame.to_ndarray(format="bgr24")

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
        