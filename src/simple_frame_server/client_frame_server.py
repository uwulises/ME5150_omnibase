import asyncio
import websockets
import base64
import io
from PIL import Image
import numpy as np
import cv2

async def receive_video():
    async with websockets.connect('ws://192.168.255.199:8765') as websocket:
        while True:
            # Receive the frame from the server
            encoded_frame = await websocket.recv()

            # Decode and process the frame
            image_bytes = base64.b64decode(encoded_frame)
            np_array = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            # Display the frame
            cv2.imshow("Video", frame)
            cv2.waitKey(1)

# Run the client
asyncio.get_event_loop().run_until_complete(receive_video())
