from flask import Flask, render_template, g
from flask_socketio import SocketIO, emit
import cv2

app = Flask(__name__)
socketio = SocketIO(app)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
camera = None
#--------------------------------------------------------------
def open_camera():
    #Here we open the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error al abrir la camara")
        return None 
    return cap 

def capture_operations(cap):

    # Here we do the cv capture procedure...
    while True:
        # Take frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
        
        # Verify capture status --> to do
        # if not ret:
        #     print("Error al capturar el frame.")
        #     break

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Face', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()

        # Show frame and emit for socket.io 
        #cv2.imshow("Captura", frame)
        emit('new_frame', {'frame': frame_data}, broadcast=True)

        
def close_camera(cap):
    # Liberar la captura de video
    cap.release()

#--------------------------------------------------------------


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('camera_function')
def camera_start(data):
    
    is_enabled = data.get('is_enabled')

    if is_enabled:
        global camera 
        camera = open_camera()
        if camera is not None:
            capture_operations(camera)
    else:
        camera.release()


if __name__ == '__main__':
    socketio.run(app, debug=True)
