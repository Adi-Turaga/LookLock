import cv2
import face_recognition
from imutils import paths
import pickle
import os
import binascii

class Encoder:
    def __init__(self, vid_ptr, encodings_file, faces_db, name, detection_method="hog", num_pics=6, channel=0):
        self.vid = vid_ptr
        self.name = name
        self.encodings_file = encodings_file
        self.faces_db = faces_db
        self.detection_method = detection_method
        self.num_pics = num_pics
        self.channel = channel
        self._path = os.path.join(faces_db, self.name)
        self.pic_names = []

    def gen_pic_names(self):
        for i in range(self.num_pics):
            _img = "{}/{}.png".format(self._path, str(binascii.b2a_hex(os.urandom(15))))
            self.pic_names.append(_img)
        return self.pic_names
    
    def is_empty(self):
        return os.stat(self.encodings_file).st_size == 0
    
    def create_dir_if_needed(self):
        if os.path.exists(self._path) == False: os.mkdir(self._path)
        else: pass

    def encode_face(self):
        pics = self.gen_pic_names()
        for pic in pics:
            print("Press p to take picture")
            while True:
                ret, frame = self.vid.read()
                cv2.imshow('Webcam feed', frame)
                if cv2.waitKey(1) & 0xFF == ord('p'):
                    cv2.imwrite(pic, frame)
                    print("Picture taken, now try different angle")
                    break

        imagePaths = list(paths.list_images(self._path))
        print(imagePaths)

        for(i, imagePath) in enumerate(imagePaths):
            print("[INFO] processing image {}/{}".format(i+1, len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            print(name)

            boxes = face_recognition.face_locations(rgb, model=self.detection_method)
            encodings = face_recognition.face_encodings(rgb, boxes)

            if self.is_empty() == False:
                enc_data = pickle.loads(open(self.encodings_file, "rb").read())
                for encoding in encodings:
                    enc_data["encodings"].append(encoding)
                    enc_data["names"].append(name)
                    print(name)
                    print(encoding)
        
            elif self.is_empty() == True:
                known_encodings = []
                known_names = []
                for encoding in encodings:
                    known_encodings.append(encoding)
                    known_names.append(name)
                enc_data = {"encodings": known_encodings, "names": known_names}
                print(enc_data)

            print("[INFO] updating database...")
            f = open(self.encodings_file, "wb")
            f.write(pickle.dumps(enc_data))
            f.close()

            print("Face encoded!")