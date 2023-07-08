import asyncio
import websockets
import base64
import picamera
import io
import time

async def send_video(websocket, path):
    # Set up the Raspberry Pi camera
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    time.sleep(1)

    frame_count = 0
    max_frame_count = 2  # Number of frames to skip before sending a frame

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

            try:
                # Send the frame to the client
                await websocket.send(encoded_image)
            except websockets.exceptions.ConnectionClosed:
                # Connection closed by the client
                print("Client connection closed")
                break

            # Delete the captured frame
            stream.close()

    finally:
        # Clean up resources
        camera.close()

async def start_server():
    server = await websockets.serve(send_video, '0.0.0.0', 8765)

    # Keep the server running until interrupted
    await server.wait_closed()

asyncio.run(start_server())
