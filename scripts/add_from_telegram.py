import cv2
from core.lbph_recognizer import LBPHRecognizer
from pathlib import Path

name = Path("data/pending/name.txt").read_text().strip()
img = cv2.imread("data/pending/unknown.jpg", cv2.IMREAD_GRAYSCALE)

person_dir = Path(f"data/known_faces/{name}/train")
person_dir.mkdir(parents=True, exist_ok=True)

cv2.imwrite(str(person_dir / f"{name}_001.jpg"), img)

LBPHRecognizer().train_from_dataset("data/known_faces")
print("✅ New face added:", name)
