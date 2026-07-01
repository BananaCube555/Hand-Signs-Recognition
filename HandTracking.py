import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import time

# -------------------------
# Create detector
# -------------------------
base_options = python.BaseOptions( 
    model_asset_path="hand_landmarker.task" # Loads pre trained model that is needed for the script to work "hand_landmarker.task"
)

options = vision.HandLandmarkerOptions( #Configures the settings
    base_options=base_options,#Path to the model , ...
    num_hands=2   # Max hands that the model should detect 
)

detector = vision.HandLandmarker.create_from_options(options)#Makes an object with the above settings conf

# -------------------------
# Webcam (MERGED PART)   Access_Webcam.py
# -------------------------

cap = cv2.VideoCapture(0) # Opens your default cammera, starts streaming frames

# Skeleton graph points  
# the connections used for the hands ex. 5 - 8 index finger

connections = [
    (0,1),(1,2),(2,3),(3,4), 
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

frames = []
countdown = False
capture = False
target_frames = 3
session = None

cv2.namedWindow("Hand Landmarks", cv2.WINDOW_NORMAL) # Lets you resize the widnow by code or by mouse
cv2.resizeWindow("Hand Landmarks", 640, 480) # Sets widnow size

while True:

    ret, frame = cap.read() # Ret is Boolean(True/False) that tells us if the frame was succefully captured, frame is the actuall image that contains the pixel data, cap.read captures the frame
    if not ret: # Check if the frame was captured if not break the loop(live feed)
        break 

    # -------------------------
    # Convert OpenCV → MediaPipe Image
    # -------------------------
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #We conver from BGR(Blue, green, red) which was the way the model was trained to rgb(red, green, blue) 

    mp_image = mp.Image(  #We use mp.Image bc we need to give the ann more than the numpy array of pixels.(Rgb array, format metadata, ...)
        image_format=mp.ImageFormat.SRGB,  #Doesnt covert or change the pixels in any away just tells mediaPipe how to read the data correcly 
        data=rgb_frame 
    )

    Allpoints = []

    # -------------------------
    # Detect hands
    # -------------------------
    result = detector.detect(mp_image) # Return the result from the model ex. Detected or not, how many hands were detected...

    h, w, _ = frame.shape # The pos of each fingere come in percentage so using the width and the height of your screen we get how big the image is

    # -------------------------
    # Draw landmarks
    # -------------------------

    H1points = []
    H2points = []

    if result.hand_landmarks: # Continue if the ann has detected a hand. result.hand... is a list hand1,hand2,.. so it checks if its empty
        for hand_index, hand in enumerate(result.hand_landmarks): #Loops through each hand 

            points = [] 

            for landmark in hand: # Each landmark is one join (thumb, index finger ,ect)

                x = int(landmark.x * w) # we covert from a percentage to px
                y = int(landmark.y * h)

                points.append((x, y))
                Allpoints.append((x, y))

                if hand_index == 0:
                    H1points.append((x, y))

                if hand_index == 1:
                    H2points.append((x, y))

                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1) # Draws a point (x, y) will be the center of it

            for start, end in connections: # Line 31
                cv2.line(  #Draw a line
                    frame,
                    points[start],
                    points[end],
                    (255, 0, 0),
                    2 #You can adjust the thickness
                )

    if countdown:
        elapsed = time.time() - start_time
        remaining = 3 - int(elapsed)

        if remaining > 0:
            cv2.putText(frame, str(remaining), (300, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 255), 5)
        else:
            countdown = False
            capture = True


    if capture:
        if len(H1points) == 21 or len(Allpoints) ==  42: #Check 
            frames.append(Allpoints.copy())

        if len(frames) >= target_frames:
            print("\nSESSION DONE")
            print(frames)

            capture = False
            frames = []

    
    cv2.imshow("Hand Landmarks", frame)
    

    key = cv2.waitKey(1) & 0xFF

    if key == ord("1"):
        countdown = True
        start_time = time.time() 
        frames = []

    if key == ord("q"):
        break


cap.release()  #Closes the webcam
cv2.destroyAllWindows() #Closes all Cv widnows




