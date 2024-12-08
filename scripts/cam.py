import cv2
import os

# For testing, stream a video instead of the camera frames
current_dir = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(current_dir, "video.mp4")
camera = cv2.VideoCapture(video_path)

# # Initialize the camera (default index 0, or provide the correct index if needed)
# camera = cv2.VideoCapture(0)  # Use 0 for the default camera (you can change this if you have multiple cameras)

def capture_frame():
    success, frame = camera.read()

    if not success:
        return None
    return frame
