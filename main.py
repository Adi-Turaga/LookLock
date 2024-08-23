import LookLock
from LookLock import Encoder, Recognizer, Gui, Liveness
import cv2
import os
import pwd

username = pwd.getpwuid(os.getuid())[0]

# recognition variables
encodings_file = "/home/{}/LookLock/encodings/faces.dat".format(username)
detection_method = "hog"
channel = 0

# encoding variables
faces_db = "/home/{}/LookLock/.cache/faces/".format(username)
num_pics = 6

# liveness variables
model = "/home/{}/LookLock/Liveness-files/model.h5".format(username)
labels = "/home/{}/LookLock/Liveness-files/labels.dat".format(username)
ld = Liveness(model, labels)

vid = cv2.VideoCapture(channel)

if __name__ == "__main__":
    while True:
        while True:

            ret, frame = vid.read()
            cv2.imshow('Webcam feed', frame)
            key_press = cv2.waitKey(1) & 0xFF

            if key_press == ord('r'):
                img_name = Recognizer.gen_pic_name()
                cv2.imwrite(img_name, frame)

                try:
                    is_real = ld.detect_liveness(img_name)
                    print(is_real)

                    if is_real == False:
                        print("[ERROR] Spoof detected...try again if not the case")
                        os.remove(img_name)
                        continue

                    result, name = Recognizer.recognize_face(img_name, encodings_file)
                    if result == True:
                        print("Recognized {}".format(name))

                except Exception as e:
                    print("[ERORR] An error occured: {}".format(e))
                    os.remove(img_name)

            elif key_press == ord('e'):
                name = Gui.prompt_name()
                encoder = Encoder(vid, encodings_file, faces_db, name)
                encoder.create_dir_if_needed()
                encoder.encode_face()
            
            elif key_press == ord('q'):
                cv2.destroyAllWindows()
                print("Program terminated...have a great day")
                exit()