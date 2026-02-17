import cv2
import time
from pathlib import Path

from core.camera import Camera
from core.detector import FaceDetector
from core.lbph_recognizer import LBPHRecognizer

PHOTO_COUNT = 25
SAVE_SIZE = (200, 200)

def add_new_face(person_name: str):
    base_dir = Path("data/known_faces")
    person_dir = base_dir / person_name

    train_dir = person_dir / "train"
    color_dir = person_dir / "color"

    train_dir.mkdir(parents=True, exist_ok=True)
    color_dir.mkdir(parents=True, exist_ok=True)

    cam = Camera()
    detector = FaceDetector()

    print(f"[ADD FACE] Capturing FULL FACE photos for: {person_name}")
    captured = 0

    try:
        while captured < PHOTO_COUNT:
            ret, frame = cam.read()
            if not ret:
                continue

            # ✅ VERY IMPORTANT: freeze frame (prevents glitch)
            frame = frame.copy()

            h_img, w_img, _ = frame.shape

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detect(gray)

            if faces is None or len(faces) == 0:
                continue

            # pick biggest face
            faces = sorted(
                faces,
                key=lambda b: (b[2] - b[0]) * (b[3] - b[1]),
                reverse=True,
            )

            x1, y1, x2, y2 = faces[0]
            face_w = x2 - x1
            face_h = y2 - y1

            # ❌ reject far / partial faces
            if face_w < 160 or face_h < 160:
                continue

            # 🔥 FULL FACE padding (25%)
            pad = int(0.25 * face_w)

            x1p = max(0, x1 - pad)
            y1p = max(0, y1 - pad)
            x2p = min(w_img, x2 + pad)
            y2p = min(h_img, y2 + pad)

            face_color = frame[y1p:y2p, x1p:x2p]
            if face_color.size == 0:
                continue

            # ---------- TRAIN IMAGE ----------
            face_gray = cv2.cvtColor(face_color, cv2.COLOR_BGR2GRAY)
            face_gray = cv2.resize(face_gray, SAVE_SIZE)
            face_gray = cv2.equalizeHist(face_gray)

            train_path = train_dir / f"{person_name}_{captured+1:03d}.jpg"
            cv2.imwrite(str(train_path), face_gray)

            # ---------- COLOR IMAGE ----------
            color_path = color_dir / f"{person_name}_{captured+1:03d}.jpg"
            cv2.imwrite(str(color_path), face_color)

            captured += 1
            print(f"📸 Saved {captured}/{PHOTO_COUNT}")
            time.sleep(0.35)

    finally:
        cam.release()

    print("✅ Face capture complete")

    # ---------- RETRAIN ----------
    recognizer = LBPHRecognizer()
    recognizer.train_from_dataset("data/known_faces")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m scripts.add_face_automation <PersonName>")
    else:
        add_new_face(sys.argv[1])
