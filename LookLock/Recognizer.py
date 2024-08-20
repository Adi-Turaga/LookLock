import cv2
import face_recognition
import pickle
import binascii
import os

class Recognizer:

    @staticmethod
    def gen_pic_name():
        img_name = "{}.png".format(str(binascii.b2a_hex(os.urandom(15))))
        return img_name

    @staticmethod
    def recognize_face(image, faces_dat, detection_method="hog"):
        _img = cv2.imread(image)
        rgb = cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
        _data = pickle.loads(open(faces_dat, "rb").read())

        os.remove(image)

        boxes = face_recognition.face_locations(rgb, model=detection_method)
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        name = ""

        for encoding in encodings:
            matches = face_recognition.compare_faces(_data["encodings"], encoding)
            name = "Unknown"
            
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                
                for i in matchedIdxs:
                    name = _data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                    
                name = max(counts, key=counts.get)
            names.append(name)

        if name == 'Unknown': return [False, "unknown"]
        elif name == "": return [False, None]
        else: return [True, name]