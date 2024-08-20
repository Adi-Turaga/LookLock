import LookLock
from LookLock import Encoder, Recognizer, Gui
import cv2
import os

# recognition variables
encodings_file = "/home/adi/LookLock/encodings/faces.dat"
detection_method = "hog"
channel = 0

# encoding variables
faces_db = "/home/adi/LookLock/.cache/faces/"
num_pics = 6

vid = cv2.VideoCapture(channel)

while True:
    while True:
        ret, frame = vid.read()
        cv2.imshow('Webcam feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('r'):
            img_name = Recognizer.gen_pic_name()
            cv2.imwrite(img_name, frame)
            try:
                result, name = Recognizer.recognize_face(img_name, encodings_file)
                if result == True:
                    print("Recognized {}".format(name))
            except Exception as e:
                print("[ERORR] An error occured: {}".format(e))
                os.remove(img_name)

        elif cv2.waitKey(1) & 0xFF == ord('e'):
            name = Gui.prompt_name()
            encoder = Encoder(vid, encodings_file, faces_db, name)
            encoder.create_dir_if_needed()
            encoder.encode_face()
        
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            print("Program terminated...have a great day")
            exit()