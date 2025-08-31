import cv2
from keras.models import model_from_json
import numpy as np
import os

MODEL_JSON = "emotiondectector.json"
MODEL_WEIGHTS = "emotiondectector.h5"

with open(MODEL_JSON, "r") as json_file:
    model_json = json_file.read()
model = model_from_json(model_json)
model.load_weights(MODEL_WEIGHTS)

haar_file = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(haar_file)

def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

webcam = cv2.VideoCapture(0)
labels = {0:"angry",1:"disgust",2:"fear",3:"happy",4:"neutral",5:"sad",6:"surprise"}

while True:
    ret, frame = webcam.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        try:
            face_resized = cv2.resize(face, (48, 48))
            img = extract_features(face_resized)
            pred = model.predict(img)
            prediction_label = labels[pred.argmax()]
            cv2.putText(frame, prediction_label, (x, y - 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0,0,255), 2)
        except:
            continue
    cv2.imshow("Face Emotion Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

webcam.release()
cv2.destroyAllWindows()
