import face_recognition
import cv2
import pickle
import traceback
import os
import sys
import psycopg2
ids=[]
try:
    conn = psycopg2.connect(database='Facelogin', user='postgres', password="8109556911", host='localhost')
    print("Database Connection : Done")
    cur = conn.cursor()
    cur.execute("select * from names")
    nameas1 = cur.fetchall()
    for row in nameas1:
        ids.append(row[0])
except Exception:
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)
    del exc_info

input_video = cv2.VideoCapture(0)
known_faces = []


face_locations = []
face_encodings = []
face_names = []
frame_number = 0

id1 = ids[-1]+1
print("Your have given ID = ", id1)
while True:
    ret, frame = input_video.read()
    frame_number += 1
    if not ret:
        break
    rgb_frame = frame[:, :, ::-1]
    all_face_encodings={}
    with open('dataset_faces.dat', 'rb') as f:
    	all_face_encodings = pickle.load(f)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    if face_encodings!=[]:
        all_face_encodings[id1]=face_encodings
        known_faces.append(face_encodings)
        result = all_face_encodings.pop(4, "None")
        result = all_face_encodings.pop(5, "None")
        result = all_face_encodings.pop(6, "None")
        result = all_face_encodings.pop(7, "None")
        with open('dataset_faces.dat', 'wb') as f:
            pickle.dump(all_face_encodings, f)
        input_video.release()
        cv2.destroyAllWindows()
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(all_face_encodings)
input_video.release()
cv2.destroyAllWindows()
