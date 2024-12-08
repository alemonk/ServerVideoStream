import asyncio
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import json
from websockets.asyncio.server import serve
import websockets.exceptions
from threading import Thread
from scripts.gpio import GPIOHandler
from scripts import cam
import cv2
from io import BytesIO
from PIL import Image

HOST = "192.168.1.93"
HTTP_PORT = 80
WEBSOCKET_PORT = 8888

# Directory to serve static files
STATIC_DIR = "./static"

# Shared state for the toggle
TOGGLE_STATE = {"state": False}  # False = OFF, True = ON

# Setup GPIO
gpio_handler = GPIOHandler()

class NeuralHTTP(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/state":
            # Serve the current toggle state (legacy endpoint)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(TOGGLE_STATE), "utf-8"))
            
        elif self.path == "/image_frame":
            # Serve the current camera frame
            frame = cam.capture_frame()
            if frame is None:
                self.send_error(500, "Failed to capture frame")
                return

            # Convert the frame to JPEG
            _, buffer = cv2.imencode('.jpg', frame)

            # Send the image as the HTTP response
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            self.wfile.write(buffer.tobytes())

        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/toggle":
            # Handle toggle state change (legacy endpoint)
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(post_data)
            update_state(data.get("state", False))
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"status": "success", "state": TOGGLE_STATE["state"]}), "utf-8"))
        else:
            self.send_error(404, "Endpoint not found")

def update_state(new_state):
    """
    Update the toggle state and notify WebSocket clients.
    """
    TOGGLE_STATE["state"] = new_state
    print(f"Toggle state updated to: {TOGGLE_STATE['state']}")
    gpio_handler.set_gpio_26(new_state)

    # Schedule notify_clients without blocking the event loop
    asyncio.create_task(notify_clients(new_state))

# List of connected WebSocket clients
connected_clients = set()

async def websocket_handler(websocket):
    connected_clients.add(websocket)
    try:
        await websocket.send(json.dumps(TOGGLE_STATE))
        async for message in websocket:
            data = json.loads(message)
            if "state" in data:
                update_state(data["state"])
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket connection closed: {e}")
    finally:
        connected_clients.remove(websocket)
        print(f"Removed WebSocket {websocket}")

async def notify_clients(state):
    """
    Notify all connected WebSocket clients about a state change.
    """
    if connected_clients:
        message = json.dumps({"state": state})
        tasks = []
        for client in connected_clients:
            try:
                tasks.append(asyncio.create_task(client.send(message)))
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Failed to notify a client: {e}")
                connected_clients.remove(client)
        await asyncio.gather(*tasks, return_exceptions=True)

def run_http_server():
    os.chdir(STATIC_DIR)  # Serve static files
    server = HTTPServer((HOST, HTTP_PORT), NeuralHTTP)
    print(f"HTTP server running on http://{HOST}:{HTTP_PORT}")
    server.serve_forever()

async def run_websocket_server():
    print(f"WebSocket server running on ws://{HOST}:{WEBSOCKET_PORT}")
    async with serve(websocket_handler, HOST, WEBSOCKET_PORT, ping_interval=20, ping_timeout=60) as server:
        await server.serve_forever()

if __name__ == "__main__":
    # Run HTTP server in a separate thread
    http_thread = Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Run WebSocket server in the main asyncio event loop
    asyncio.run(run_websocket_server())
