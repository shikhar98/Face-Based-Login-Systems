from flask import Flask,render_template,url_for,request,redirect
import face_recognition
import cv2
import pickle
import traceback
import os
import sys
import psycopg2

try:
    conn = psycopg2.connect(database='Facelogin', user='postgres', password="8109556911", host='localhost')
    print("Database Connection : Done")
    cur = conn.cursor()
except Exception:
    exc_info = sys.exc_info()
    traceback.print_exception(*exc_info)
    del exc_info
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/signup',methods=['POST'])
def signup():
    ids=[]
    try:
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

    id1 = ids[-1] + 1
    print("Your have given ID = ", id1)
    while True:
        ret, frame = input_video.read()
        frame_number += 1
        if not ret:
            break
        rgb_frame = frame[:, :, ::-1]
        all_face_encodings = {}
        with open('dataset_faces.dat', 'rb') as f:
            all_face_encodings = pickle.load(f)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        if face_encodings != []:
            all_face_encodings[id1] = face_encodings
            known_faces.append(face_encodings)
            with open('dataset_faces.dat', 'wb') as f:
                pickle.dump(all_face_encodings, f)
            cv2.imshow('Video', frame)
            uname = request.form['uname']
            try:
                cur.execute("insert into names (id,name) values (%s,%s);",(id1,uname,))
                conn.commit()
            except Exception:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                del exc_info
            input_video.release()
            cv2.destroyAllWindows()
            del input_video
            return render_template('login.html', name=uname)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(all_face_encodings)
    input_video.release()
    cv2.destroyAllWindows()

@app.route('/predict',methods=['POST'])
def predict():
    import face_recognition
    import cv2
    import pickle
    input_video = cv2.VideoCapture(0)
    with open('dataset_faces.dat', 'rb') as f:
        all_face_encodings = pickle.load(f)
    known_faces = []
    for values in all_face_encodings.values():
        values = values[0]
        known_faces.append(values)
    face_locations = []
    face_encodings = []
    face_names = []
    frame_number = 0
    names = []
    try:
        cur.execute("select * from names")
        nameas1 = cur.fetchall()
        for row in nameas1:
            names.append(row[1])
    except Exception:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        del exc_info
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
            c = 0
            i = 0
            for j in match:
                if match[c]:
                    face_names.append(names[c])
                else:
                    c = c + 1
                i = i + 1
            if i == c:
                face_names.append('Not-Known')
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if i!=c:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
                cv2.imshow('Video', frame)
                input_video.release()
                cv2.destroyAllWindows()
                del input_video
                path = '/static/Images'
                cv2.imwrite(os.path.join(path , 'User.jpg'), frame)
                return render_template('login.html', name=name)
            else:
                input_video.release()
                cv2.destroyAllWindows()
                del input_video
                return render_template('signup.html')
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    input_video.release()
    cv2.destroyAllWindows()
    del input_video

if __name__=='__main__':
    app.run(debug=True)