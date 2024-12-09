import cv2
import time
import subprocess
from datetime import datetime
from PIL import Image
import os

def capture_single_image():
    try:
        # Define the output file path
        output_file = os.path.join(os.getcwd(), "img.jpg")
        print(output_file)
        
        # Define the libcamera-jpeg command
        command = [
            "libcamera-jpeg",
            "--nopreview",
            "-o", output_file,
            "--width", "1920",  # Optional: Specify resolution
            "--height", "1080"  # Optional: Specify resolution
        ]
        
        # Run the command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Save the current date and time in time.txt
        timestamp_file = os.path.join(os.getcwd(), "time.txt")
        with open(timestamp_file, "w") as f:
            current_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            f.write(current_time)
            print(f"Timestamp saved: {current_time}")
        
        # Load the image using PIL
        with open(output_file, "rb") as f:
            image = Image.open(f)
        
        # Return the PIL Image object
        return image
    except subprocess.CalledProcessError as e:
        print("Error while executing command:")
        print(e.stderr.decode('utf-8'))
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None

class CameraCapture:
    def __init__(self):
        print("Initializing CameraCapture...")

        self.camera = cv2.VideoCapture(0)
        # self.camera.set(3,640) # Width
        # self.camera.set(4,480) # Height
        # self.camera.set(10,100) # Brightness
        
        if self.camera.isOpened():
            print("Camera successfully initialized.")
        else:
            raise RuntimeError("Error: Camera initialization failed.")

    def capture_frame(self):
        """
        Capture a single frame from the camera.

        :return: The captured frame as a NumPy array, or None if the capture fails.
        """
        success, frame = self.camera.read()

        if not success:
            print("Error: Failed to read frame from camera.")
            return None
        if frame is None:
            print("Error: Frame is None.")
            return None
        return frame

    def release_camera(self):
        """
        Release the camera resource.
        """
        if self.camera.isOpened():
            self.camera.release()
            print("Camera released.")

# Example usage:
if __name__ == "__main__":
    camera = CameraCapture()
    while True:
        frame = camera.capture_frame()
        if frame is not None:
            cv2.imshow("Camera Frame", frame)
            cv2.imwrite("img.png", frame)
            if cv2.waitKey(1000) & 0xFF == ord('q'):  # Quit on 'q' key press
                break
        time.sleep(1)
    camera.release_camera()
    cv2.destroyAllWindows()
