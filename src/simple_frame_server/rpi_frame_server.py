import asyncio
import websockets
import base64
import picamera
import io

async def send_video(websocket, path):
    # Set up the Raspberry Pi camera
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)

    frame_count = 0
    max_frame_count = 5  # Number of frames to skip before sending a frame

    try:
        # Continuously capture and send video frames
        while True:
            # Capture a frame
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg', use_video_port=True)

            # Skip frames according to the frame count
            frame_count += 1
            if frame_count % max_frame_count != 0:
                # Delete the captured frame without sending it
                stream.close()
                continue

            # Read the captured frame
            stream.seek(0)
            encoded_image = base64.b64encode(stream.read()).decode('utf-8')

            # Send the frame to the client
            await websocket.send(encoded_image)

            # Delete the captured frame
            stream.close()

    finally:
        # Clean up resources
        camera.close()

start_server = websockets.serve(send_video, '0.0.0.0', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()