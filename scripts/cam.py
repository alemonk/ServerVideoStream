import cv2
import time

class CameraCapture:
    def __init__(self):
        print("Initializing CameraCapture...")

        self.camera = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.camera.set(3,640) # Width
        self.camera.set(4,480) # Height
        self.camera.set(10,100) # Brightness

        self.pipeline = (
            "libcamerasrc ! video/x-raw,width=640,height=480,format=BGR ! "
            "videoconvert ! appsink"
        )
        self.camera = cv2.VideoCapture(self.pipeline, cv2.CAP_GSTREAMER)

        if not self.camera.isOpened():
            print("Pipeline:", self.pipeline)
            raise RuntimeError("Error: Could not open camera with the given pipeline.")

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
