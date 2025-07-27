import cv2
import subprocess # connection of two different .py file 

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print(" Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow(' Video ', frame)

    if cv2.waitKey(1) == ord('x'):  # Press 'x' to capture
        cv2.imwrite("webcam_capture.png", frame)
        print("Image captured and saved")
        break
      
 cap.release()
