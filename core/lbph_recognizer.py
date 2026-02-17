import cv2
import os

class LBPHRecognizer:
    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.labels = {} # Empty Dictionary

    def load(self):
        model_path = "data/lbph/lbph_model.yml"
        label_path = "data/lbph/labels.txt"

        if not os.path.exists(model_path) or not os.path.exists(label_path):
            print("❌ Model or Labels missing.")
            return

        # Load Brain
        self.recognizer.read(model_path)

        # 🔥 FIX: Robust Label Loading
        # Reads "0,Charith" -> {0: "Charith"}
        self.labels = {}
        with open(label_path, "r") as f:
            for line in f:
                line = line.strip()
                if "," in line:
                    parts = line.split(",")
                    # Force ID to be Integer (Critical Fix)
                    face_id = int(parts[0]) 
                    name = parts[1]
                    self.labels[face_id] = name
        
        print(f"[INFO] Loaded Labels: {self.labels}")

    def predict(self, face_img):
        try:
            # Predict returns (id, confidence)
            # Confidence: 0 = Exact Match, 100 = Total Opposite
            label_id, confidence = self.recognizer.predict(face_img)
            
            # 🔥 FIX: Safe Name Lookup
            if label_id in self.labels:
                name = self.labels[label_id]
            else:
                name = "UNKNOWN"
            
            return name, confidence
        except Exception as e:
            return "UNKNOWN", 100