import cv2 as cv

# Open webcam (0 = default camera)
cap = cv.VideoCapture(0)

# Or open a video file
# cap = cv.VideoCapture('video.mp4')

while True:
    # Read frame
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Convert to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # Display
    cv.imshow('Webcam', gray)
    
    # Break on 'q' key
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()