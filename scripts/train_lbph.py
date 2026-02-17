import cv2
import numpy as np
from pathlib import Path

DATASET_DIR = Path("data/known_faces")
MODEL_DIR = Path("data/lbph")
MODEL_PATH = MODEL_DIR / "lbph_model.yml"
LABELS_PATH = MODEL_DIR / "labels.txt"

CASCADE_PATH = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"


def extract_face(gray, face_cascade):
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))
    if len(faces) == 0:
        return None

    # take biggest face
    faces = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
    x, y, w, h = faces[0]
    face = gray[y:y+h, x:x+w]
    face = cv2.resize(face, (200, 200))
    return face


def main():
    print("[INFO] Training LBPH model (FACE-CROP only)...")

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    if face_cascade.empty():
        print("❌ Haar cascade not loaded")
        return

    faces = []
    labels = []
    label_map = {}
    current_label = 0

    for person_dir in DATASET_DIR.iterdir():
        if not person_dir.is_dir():
            continue

        name = person_dir.name
        if name not in label_map:
            label_map[name] = current_label
            current_label += 1

        label_id = label_map[name]
        print(f"\n[INFO] Person: {name}")

        for img_path in person_dir.rglob("*.*"):
            if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
                continue

            img = cv2.imread(str(img_path))
            if img is None:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            face = extract_face(gray, face_cascade)
            if face is None:
                print(f"  -> {img_path.name}  [SKIP: no face]")
                continue

            faces.append(face)
            labels.append(label_id)
            print(f"  -> {img_path.name}  [OK]")

    if len(faces) < 6:
        print("\n❌ Not enough face images for training. Capture more clear pics.")
        return

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    recognizer.save(str(MODEL_PATH))

    with open(LABELS_PATH, "w") as f:
        for name, idx in label_map.items():
            f.write(f"{idx},{name}\n")

    print(f"\n✅ Model saved: {MODEL_PATH}")
    print(f"✅ Labels saved: {LABELS_PATH}")
    print(f"[INFO] Trained with {len(faces)} face-cropped images")


if __name__ == "__main__":
    main()
