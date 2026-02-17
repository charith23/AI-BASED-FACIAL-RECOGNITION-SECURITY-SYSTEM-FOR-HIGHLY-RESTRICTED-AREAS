# core/liveness.py
import cv2

class LivenessDetector:
    def __init__(self):
        # Load Pre-trained Eye Model (Built-in OpenCV)
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

    def detect_blink(self, face_img):
        # Detect eyes in the face region
        eyes = self.eye_cascade.detectMultiScale(face_img, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
        
        # If eyes detected -> Eyes Open
        # If no eyes detected (but face is there) -> Possible Blink
        return len(eyes)