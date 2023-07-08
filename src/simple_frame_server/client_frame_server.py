import asyncio
import websockets
import base64
import cv2
import numpy as np

async def receive_video():
    async with websockets.connect('ws://omni.local:8765',ping_interval=None) as websocket:
        try:
            while True:
                # Receive the frame from the server
                encoded_image = await websocket.recv()

                # Decode the base64 encoded frame
                decoded_image = base64.b64decode(encoded_image)

                # Convert the frame to NumPy array
                np_arr = np.frombuffer(decoded_image, dtype=np.uint8)

                # Decode the image array using OpenCV
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                # Display the frame
                cv2.imshow('Video Stream', frame)
                if cv2.waitKey(1) == 27:
                    break

        finally:
            cv2.destroyAllWindows()

# Start the video stream reception
asyncio.get_event_loop().run_until_complete(receive_video())
