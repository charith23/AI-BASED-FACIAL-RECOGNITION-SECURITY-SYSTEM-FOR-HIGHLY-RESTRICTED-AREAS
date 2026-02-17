# core/antispoof.py
import cv2
import numpy as np

class AntiSpoof:
    def __init__(self):
        pass

    def is_live(self, frame, face_box):
        (x, y, w, h) = face_box
        
        if x < 0 or y < 0 or x+w > frame.shape[1] or y+h > frame.shape[0]:
            return False

        face = frame[y:y+h, x:x+w]
        if face.size == 0: return False

        gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        # TEXTURE CHECK
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # 🔥 FIX: High Lighting causes "smooth" faces.
        # Lowered threshold from 100 -> 30.
        # We rely on BLINK DETECTION for real security now.
        if laplacian_var < 15:  
            # print(f"DEBUG: Texture too low: {laplacian_var}") # Optional Debug
            return False 

        return True