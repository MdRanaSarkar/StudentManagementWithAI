from SFaceRecognize.models import Detected
from student.models import CustomUser, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, \
    LeaveReportStudent, FeedBackStudent, StudentResult
import cv2
import pickle
import face_recognition
import datetime
from cachetools import TTLCache
from django.utils import timezone
from django.shortcuts import render,get_list_or_404,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import  reverse

cache = TTLCache(maxsize=20, ttl=10)


def identify1(frame, name, buf, buf_length, known_conf):
    if name in cache:
        return
    count = 0
    for ele in buf:
        count += ele.count(name)

    if count >= known_conf:
        timestamp = datetime.datetime.now(tz=timezone.utc)
        print(name, timestamp)


        cache[name] = 'detected'
        path = 'SFaceRecognize/FRStream/detected/{}_{}.jpg'.format(name, timestamp)
        cv2.imwrite(path, frame)
        try:
            stdd = Students.objects.get(name=name)
            stdd.detected_set.create(time_stamp=timestamp)
        except:
            pass


def predict(rgb_frame, knn_clf=None, model_path=None, distance_threshold=0.5):
    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)
    X_face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=2)
    if len(X_face_locations) == 0:
        return []
    faces_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
    # print(closest_distances)
    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in
            zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


def identify_faces(video_capture,stdinfo):
    buf_length = 10
    known_conf = 5
    buf = [[]] * buf_length
    i = 0

    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            predictions = predict(rgb_frame, model_path="SFaceRecognize/FRStream/Model/trained_model.clf")
            # print(predictions)

        process_this_frame = not process_this_frame

        face_names = []
        username=""

        for name, (top, right, bottom, left) in predictions:
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

            identify1(frame, name, buf, buf_length, known_conf)

            face_names.append(name)
            username=name

        buf[i] = face_names
        i = (i + 1) % buf_length


        # print(buf)

        # Display the resulting image
        cv2.imshow('Video', frame)

        if stdinfo.admin.username==username:
            print("successfully enter")
            break
        else:
            pass

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()