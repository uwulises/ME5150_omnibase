import asyncio
import websockets
import base64
import io
from PIL import Image

async def receive_video():
    async with websockets.connect('omni.local:8765') as websocket:
        while True:
            # Receive the frame from the server
            encoded_frame = await websocket.recv()

            # Decode and display the frame
            image_bytes = base64.b64decode(encoded_frame)
            image = Image.open(io.BytesIO(image_bytes))
            image.show()

# Run the client
asyncio.get_event_loop().run_until_complete(receive_video())
