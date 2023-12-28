from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2

app = Flask(__name__)
socketio = SocketIO(app)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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

        # Romper el bucle si se presiona la tecla 'q'
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break

    # Cerrar la ventana al salir del bucle
    #cv2.destroyAllWindows()
#--------------------------------------------------------------


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('initiate_camera')
def camera_start():
    
    camera = open_camera()
    if camera is not None:
        capture_operations(camera)



if __name__ == '__main__':
    socketio.run(app, debug=True)
