import asyncio
import websockets
import base64
import io
from PIL import Image
import numpy as np
import cv2
from collections import deque
async def receive_video():
    async with websockets.connect('ws://192.168.255.199:8765') as websocket:
        frame_buffer = deque(maxlen=10)  # Buffer to store a maximum of 10 frames

        while True:
            # Receive the frame from the server
            encoded_frame = await websocket.recv()

            # Add the frame to the buffer
            frame_buffer.append(encoded_frame)

            # Process frames in the buffer
            for frame in frame_buffer:
                # Decode and display the frame
                image_bytes = base64.b64decode(frame)
                np_array = np.frombuffer(image_bytes, np.uint8)
                frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
                cv2.imshow("Video", frame)
                cv2.waitKey(1)

            # Clear the buffer
            frame_buffer.clear()

# Run the client
asyncio.get_event_loop().run_until_complete(receive_video())
