import face_recognition
import cv2
import pickle
input_video = cv2.VideoCapture(0)
with open('dataset_faces.dat', 'rb') as f:
    all_face_encodings = pickle.load(f)
known_faces=[]
for values in all_face_encodings.values():
    values=values[0]
    known_faces.append(values)
print(known_faces)
face_locations = []
face_encodings = []
face_names = []
frame_number = 0
names=['Shikhar','Siddharth Sir','Dhanu','Neha Mam']

while True:
    ret, frame = input_video.read()
    frame_number += 1
    if not ret:
        break
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)
        c=0
        print(match)
        i=0
        for j in match:
            if match[c]:
                face_names.append(names[c])
            else:
                c=c+1
            i=i+1
        if i==c:
            face_names.append('Not-Known')
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if name!="None":
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        else:
	        img3_face_encoding = face_recognition.face_encodings(frame)[0]
	        known_faces.append(img3_face_encoding)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


input_video.release()
cv2.destroyAllWindows()
