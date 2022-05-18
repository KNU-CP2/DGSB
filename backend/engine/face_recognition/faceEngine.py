import cv2
import imutils as imutils
import numpy as np
import os
import face_recognition
from imutils import paths
import pickle


class FaceRecog():
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        #self.camera = camera.VideoCamera()

        self.known_face_encodings = []
        self.known_face_names = []
        # Load sample pictures and learn how to recognize it.
        dirname = '/Users/macbook/Desktop/Project/DGSB/backend/engine/face_recognition/dataset'

        files = os.listdir(dirname)
        print(files)
        for filename in files:
            name, ext = os.path.splitext(filename)
            print(name)
            name = name.split(".")[1]
            if ext == '.jpg':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                try:
                    face_encoding = face_recognition.face_encodings(img)[0]
                except Exception:
                    print("Exception")
                    continue

                self.known_face_encodings.append(face_encoding)
                print("ongoing")
        print("complete")

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def __del__(self):
        pass
#        del self.camera

    def get_frame(self):
        # Grab a single frame of video
        #frame = self.camera.get_frame()

        # Resize frame of video to 1/4 size for faster face recognition processing
        rgb_small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        # rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 0.6 is typical best performance.
                name = "Unknown"
                print(min_value)
                if min_value < 0.37:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame

    def get_frame(self, file_name):
        # Grab a single frame of video
        frame = cv2.imread('raw/' + file_name)
        # Resize frame of video to 1/4 size for faster face recognition processing
        rgb_small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        # rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 0.6 is typical best performance.
                name = "Unknown"
                print(min_value)
                if min_value < 0.37:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]

                self.face_names.append(name)
            return self.face_names
        self.process_this_frame = not self.process_this_frame

        # Display the results
        # for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
        #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        #     top *= 4
        #     right *= 4
        #     bottom *= 4
        #     left *= 4
        #
        #     # Draw a box around the face
        #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        #
        #     # Draw a label with a name below the face
        #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #     font = cv2.FONT_HERSHEY_DUPLEX
        #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    def get_jpg_bytes(self):
        frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()



def set_detected_face(face_id, listOfImage):
    try:
        count = 0
        for file_name in listOfImage:
            rgb_small_frame = cv2.imread('raw/' + file_name)
            r = rgb_small_frame.shape[1] / float(rgb_small_frame.shape[1])
            boxes = face_recognition.face_locations(rgb_small_frame)
            # 얼굴에 대해 rectangle 출력
            try:
                for (top, right, bottom, left) in boxes:
                    # rescale the face coordinates
                    rtop = int(top * r)
                    rright = int(right * r)
                    rbottom = int(bottom * r)
                    rleft = int(left * r)
                    # draw the predicted face name on the image
                    # cv2.rectangle(frame, (rleft, rtop), (rright, rbottom),
                    #             (0, 255, 0), 2)
                    y = top - 15 if top - 15 > 15 else top + 15
                    count += 1
                    print(os.getcwd())
                    cv2.imwrite(dirname + "/User." + str(face_id) + '.' + str(count) + ".jpg", rgb_small_frame[top: bottom, left:right])
                # 종료조건
                if cv2.waitKey(1) > 0:
                    break  # 키 입력이 있을 때 반복문 종료
                elif count >= 100:
                    break  # 100 face sample
            except Exception as e:
                print(e)
                return False

        print("\n [INFO] Exiting Program and cleanup stuff")
        #learning

        dataset = dirname
        encodingDirectory = "./encoding.pickle"
        detectionMethod = "hog"

        with open(encodingDirectory, "rb") as f:
            lastData = pickle.load(f)

        print("[INFO] quantifying faces....")
        imagePaths = list(paths.list_images(dataset))
        knownEncodings = []
        knownNames = []
        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1,
                                                         len(imagePaths)))
            name = imagePath.split(".")[-3]
            # load the input image and convert it from BGR (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                knownEncodings.append(encoding)
                knownNames.append(name)
        print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open(encodingDirectory, "wb")
        f.write(pickle.dumps(data))
        f.close()
        return True
    except Exception as e:
        return False

def get_detected_face(file_name):
    face_recog = FaceRecog()
    print("start")
    print(face_recog.known_face_names)
    nameList = face_recog.get_frame(file_name)
    return nameList

if __name__ == '__main__':
    mode = int(input("모드를 선택하세요 . 1. 등록 2.학습\n"))

    if mode == 1:
        faceCascade = cv2.CascadeClassifier("./haarcascade_frontface.xml")

        capture = cv2.VideoCapture(0)

        print(capture)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        face_id = input("\n등록할 사람을 입력하세요.")
        print("\n [INFO] Initializing face capture. Look the camera and wait ...")


        count = 0  # # of caputre face images
        # 영상 처리 및 출력
        while True:
            ret, frame = capture.read()  # 카메라 상태 및 프레임
            # cf. frame = cv2.flip(frame, -1) 상하반전
            rgb_small_frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
            #rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            r = rgb_small_frame.shape[1] / float(rgb_small_frame.shape[1])

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face

            boxes = face_recognition.face_locations(rgb_small_frame)

            # 얼굴에 대해 rectangle 출력
            for (top, right, bottom, left) in boxes:
                # rescale the face coordinates
                rtop = int(top * r)
                rright = int(right * r)
                rbottom = int(bottom * r)
                rleft = int(left * r)
                # draw the predicted face name on the image
                cv2.rectangle(frame, (rleft, rtop), (rright, rbottom),
                              (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                count += 1
                cv2.imwrite(dirname + "/User." + str(face_id) + '.' + str(count) + ".jpg", rgb_small_frame[top: bottom, left:right])
            # cv2.imwrite("./dataset/User." + str(face_id) + '.' + str(count) + ".jpg", rgb)
            # count += 1
            # for (x, y, w, h) in boxes:
            #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            #     # inputOutputArray, point1 , 2, colorBGR, thickness)
            #     count += 1
            #     cv2.imwrite("./dataset/User." + str(face_id) + '.' + str(count) + ".jpg", rgb[y:y + h, x:x + w])

            cv2.imshow('image', frame)

            # 종료조건
            if cv2.waitKey(1) > 0:
                break  # 키 입력이 있을 때 반복문 종료
            elif count >= 10:
                break  # 100 face sample

        print("\n [INFO] Exiting Program and cleanup stuff")
        capture.release()  # 메모리 해제
        cv2.destroyAllWindows()  # 모든 윈도우 창 닫기

    elif mode == 2:
        from imutils import paths
        import face_recognition
        import pickle
        import cv2
        import os
        import numpy as np

        dataset = dirname
        encodingDirectory = "./encoding.pickle"
        detectionMethod = "hog"

        print("[INFO] quantifying faces....")
        data = {"encodings": [], "names": []}
        if os.path.exists(encodingDirectory):
            with open(encodingDirectory, "rb") as f:
                lastData = pickle.load(f)
            print(lastData)
            data = lastData

        imagePaths = list(paths.list_images(dataset))
        knownEncodings = data["encodings"]
        knownNames = data["names"]
        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)))
            name = imagePath.split(".")[-3]
            # load the input image and convert it from BGR (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb)
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                knownEncodings.append(encoding)
                knownNames.append(name)
        print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open(encodingDirectory, "wb")
        f.write(pickle.dumps(data))
        f.close()
    elif mode == 3:
        encodingDirectory = "./encoding.pickle"
        outputPath = "./output"
        display = 1
        detectionMethod = "hog"

        import face_recognition
        import cv2
        #import camera
        import os
        import numpy as np



        face_recog = FaceRecog()
        print("start")
        print(face_recog.known_face_names)
        while True:
            frame = face_recog.get_frame()

            # show the frame
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

        # do a bit of cleanup
        cv2.destroyAllWindows()
        print('finish')
