from keras.api.preprocessing.image import img_to_array
from keras.api.models import load_model
import numpy as np
import pickle
import cv2
import face_recognition as fr

class Liveness:

    def __init__(self, model, le):
        self._model = load_model(model)
        self._le = pickle.loads(open(le, "rb").read())

    @staticmethod
    def find_and_crop_face(img):
        frame = cv2.imread(img)
        box = fr.face_locations(frame)

        (startY, endX, endY, startX) = box[0]
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

        return frame[startY:endY, startX:endX]
    
    def detect_liveness(self, img):
        face = Liveness.find_and_crop_face(img)
        face = cv2.resize(face, (32, 32))
        face = face.astype("float") / 255.0
        face = img_to_array(face)
        face = np.expand_dims(face, axis=0)

        preds = self._model.predict(face)[0]
        j = np.argmax(preds)
        label = self._le.classes_[j]

        if label == "fake": return False
        elif label == "real": return True
        else: return None
