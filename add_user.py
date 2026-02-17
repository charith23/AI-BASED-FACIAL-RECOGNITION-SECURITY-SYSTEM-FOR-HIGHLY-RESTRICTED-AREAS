import cv2
import os
import numpy as np
from PIL import Image

# 1. SETUP
cam = cv2.VideoCapture(0, cv2.CAP_V4L2)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 2. INPUT ID
face_id = input('\nenter user id (Example: 4 for New Person): ')
print("\n [INFO] Initializing face capture. Look at the camera and wait ...")

count = 0
while(True):
    ret, img = cam.read()
    if not ret: break
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        # Save the captured image into the datasets folder
        cv2.imwrite("data/dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        print(f"Captured {count}/30")
        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff
    if k == 27: break
    elif count >= 30: # Take 30 face sample and stop video
         break

print("\n [INFO] Exiting Video and Training...")
cam.release()
cv2.destroyAllWindows()

# 3. TRAINING
print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
path = 'data/dataset'
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids

faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
recognizer.write('data/lbph/lbph_model.yml') 
print("\n [INFO] {0} faces trained. New User Added Successfully!".format(len(np.unique(ids))))
print("👉 Now restart surveillance_run.py and add the Name to the list!")