import cv2
import os
import numpy as np
from PIL import Image

def get_images_and_labels(path):
    image_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith("jpg") or file.endswith("png"):
                image_paths.append(os.path.join(root, file))

    face_samples = []
    ids = []
    name_map = {}
    current_id = 0
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    print(f"[TRAIN] Found {len(image_paths)} images.")

    for image_path in image_paths:
        try:
            # 🔥 FIX 1: Smart Name Extraction
            # If path is ".../Lalitha/train/img.jpg" -> We want "Lalitha"
            folder_name = os.path.basename(os.path.dirname(image_path))
            if folder_name == "train":
                # Go one level up
                folder_name = os.path.basename(os.path.dirname(os.path.dirname(image_path)))
            
            if folder_name not in name_map:
                name_map[folder_name] = current_id
                current_id += 1
            
            label_id = name_map[folder_name]

            # Process Image
            pil_image = Image.open(image_path).convert('L')
            img_numpy = np.array(pil_image, 'uint8')
            
            # Detect face
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                # Resize to 200x200 standard
                face_img = cv2.resize(img_numpy[y:y+h, x:x+w], (200, 200))
                face_samples.append(face_img)
                ids.append(label_id)

        except Exception as e:
            pass

    return face_samples, ids, name_map

def train():
    data_path = "data/known_faces"
    if not os.path.exists(data_path):
        print("No Data Folder.")
        return

    print("[SYSTEM] 🧠 Training Started...")
    faces, ids, names = get_images_and_labels(data_path)

    if len(faces) == 0:
        print("❌ No faces found.")
        return

    # Train
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(ids))

    os.makedirs("data/lbph", exist_ok=True)
    recognizer.write("data/lbph/lbph_model.yml")
    
    # 🔥 FIX 2: SWAP ORDER (ID, Name) to prevent crash
    with open("data/lbph/labels.txt", "w") as f:
        for name, id_ in names.items():
            f.write(f"{id_},{name}\n") # ID FIRST!

    print(f"✅ SUCCESS! Trained {len(names)} people: {list(names.keys())}")

if __name__ == "__main__":
    train()