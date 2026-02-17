# scripts/test_recognition_lbph.py
import cv2
import time

from core.camera import Camera
from core.detector import FaceDetector
from core.lbph_recognizer import LBPHRecognizer


def main():
    print("[INFO] Starting LBPH live recognition test (headless)...")

    cam = Camera(width=640, height=480, fps=30)
    cam.open()

    detector = FaceDetector()
    recognizer = LBPHRecognizer()

    frame_id = 0

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                continue

            frame_id += 1
            boxes = detector.detect(frame)

            if len(boxes) == 0:
                if frame_id % 20 == 0:
                    print(f"[FRAME {frame_id}] No face")
                continue

            # biggest face
            boxes = sorted(boxes, key=lambda b: (b[2]-b[0])*(b[3]-b[1]), reverse=True)
            x1, y1, x2, y2 = boxes[0]

            face = frame[y1:y2, x1:x2]
            face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            face_gray = cv2.resize(face_gray, (200, 200))
            # ✅ low-light improvement
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            face_gray = clahe.apply(face_gray)

            name, conf = recognizer.predict(face_gray)

            # ✅ threshold (LOW is good)
            if conf > 55:
                name = "UNKNOWN"

            print(f"[FRAME {frame_id}] Person={name}  LBPH_conf={conf:.2f}")
            time.sleep(0.02)

    finally:
        cam.release()
        print("[INFO] stopped.")


if __name__ == "__main__":
    main()
