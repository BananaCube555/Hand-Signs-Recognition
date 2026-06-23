import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Create detector
base_options = python.BaseOptions(
    model_asset_path="hand_landmarker.task"
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2
)

detector = vision.HandLandmarker.create_from_options(options)

# Load image
image_path = r"C:\Users\Marios\Downloads\Hand.png"
mp_image = mp.Image.create_from_file(image_path)

# Detect
result = detector.detect(mp_image)

# Load image with OpenCV for drawing
image = cv2.imread(image_path)

h, w, _ = image.shape

connections = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

for hand in result.hand_landmarks:

    points = []

    for landmark in hand:

        x = int(landmark.x * w)
        y = int(landmark.y * h)

        points.append((x, y))

        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

    for start, end in connections:
        cv2.line(
            image,
            points[start],
            points[end],
            (6, 6, 48, 0.45),
            2
        )
image = cv2.resize(image, (1000, 800))
cv2.imshow("Hand Landmarks", image)
cv2.waitKey(0)
cv2.destroyAllWindows()