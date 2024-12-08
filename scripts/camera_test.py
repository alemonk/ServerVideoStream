import cv2

def main():
    # Open the camera
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or specify another index
    
    if not cap.isOpened():
        print("Error: Camera not found or not accessible.")
        return
    
    print("Press 'q' to quit the camera preview.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
        
        # Display the frame in a window
        cv2.imshow("Camera Preview", frame)
        
        # Quit the preview if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
