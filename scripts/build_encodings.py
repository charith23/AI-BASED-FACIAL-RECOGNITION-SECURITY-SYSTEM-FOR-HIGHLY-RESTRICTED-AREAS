# scripts/build_encodings.py
import os
import pickle
from pathlib import Path

import cv2
import face_recognition


KNOWN_DIR = Path("data/known_faces")
OUT_FILE = Path("data/encodings/encodings.pickle")


def build_encodings():
    encodings = []
    names = []

    if not KNOWN_DIR.exists():
        raise FileNotFoundError(f"Folder not found: {KNOWN_DIR}")

    print(f"[INFO] Scanning known faces from: {KNOWN_DIR}")

    for person_dir in KNOWN_DIR.iterdir():
        if not person_dir.is_dir():
            continue

        person_name = person_dir.name
        print(f"\n[INFO] Person: {person_name}")

        for img_path in person_dir.glob("*.*"):
            if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
                continue

            print(f"  -> Processing {img_path.name}")

            image = face_recognition.load_image_file(str(img_path))
            locations = face_recognition.face_locations(image)

            if len(locations) == 0:
                print("     [WARN] No face detected. Skipping.")
                continue

            if len(locations) > 1:
                print("     [WARN] Multiple faces detected. Using first face.")

            face_encoding = face_recognition.face_encodings(image, locations)[0]
            encodings.append(face_encoding)
            names.append(person_name)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = {"encodings": encodings, "names": names}

    with open(OUT_FILE, "wb") as f:
        pickle.dump(data, f)

    print(f"\n✅ Done. Saved {len(encodings)} encodings to: {OUT_FILE}")


if __name__ == "__main__":
    build_encodings()
