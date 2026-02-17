import cv2
import os
import time

from core.camera import Camera
from core.detector import FaceDetector

SAVE_DIR = "data/known_faces/Charith/train"
os.makedirs(SAVE_DIR, exist_ok=True)

def main():
    cam = Camera()
    detector = FaceDetector()

    print("📸 Stable Face Capture Started")
    print("➡️ Keep face still, good light")
    time.sleep(2)

    count = 0
    last_frame = None

    while count < 30:
        ret, frame = cam.read()
        if not ret:
            continue

        # ---- FREEZE FRAME (KEY FIX) ----
        if last_frame is None:
            last_frame = frame.copy()
            continue

        frame = last_frame.copy()
        last_frame = None
        # --------------------------------

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = detector.detect(gray)
        if faces is None or len(faces) == 0:
            continue

        x1, y1, x2, y2 = faces[0]

        w = x2 - x1
        h = y2 - y1
        if w < 180 or h < 180:
            continue

        pad = int(0.2 * w)
        x1 = max(0, x1 - pad)
        y1 = max(0, y1 - pad)
        x2 = min(gray.shape[1], x2 + pad)
        y2 = min(gray.shape[0], y2 + pad)

        face = gray[y1:y2, x1:x2]
        face = cv2.resize(face, (200, 200))
        face = cv2.equalizeHist(face)

        fname = f"{SAVE_DIR}/Charith_{count:03}.jpg"
        cv2.imwrite(fname, face)
        print(f"✅ Saved {fname}")

        count += 1
        time.sleep(0.25)  # critical delay

    print("🎉 Capture complete")

if __name__ == "__main__":
    main()
