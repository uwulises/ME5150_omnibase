import asyncio
import websockets
import base64
import picamera
import io
async def send_video(websocket, path):
    # Set up the Raspberry Pi camera
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)

    try:
        # Continuously capture and send video frames
        while True:
            # Capture a frame
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg', use_video_port=True)

            # Read the captured frame
            stream.seek(0)
            encoded_image = base64.b64encode(stream.read()).decode('utf-8')

            # Send the frame to the client
            await websocket.send(encoded_image)
    finally:
        # Clean up resources
        camera.close()

start_server = websockets.serve(send_video, '0.0.0.0', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
