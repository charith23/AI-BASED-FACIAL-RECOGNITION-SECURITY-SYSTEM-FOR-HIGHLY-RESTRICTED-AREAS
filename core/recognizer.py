import cv2

class FaceRecognizer:
    def __init__(self):
        self.model = cv2.face.LBPHFaceRecognizer_create()
        self.labels = {}

        self.model.read("data/lbph/lbph_model.yml")
        with open("data/lbph/labels.txt") as f:
            for line in f:
                i, name = line.strip().split(",")
                self.labels[int(i)] = name

        print(f"[INFO] Loaded LBPH model + {len(self.labels)} labels")

    def predict(self, face):
        label_id, confidence = self.model.predict(face)
        name = self.labels.get(label_id, "UNKNOWN")
        return name, confidence
