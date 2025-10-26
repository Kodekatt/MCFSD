print('Setting UP')
import os
import sys

# Look for model.h5 in current directory or workspace
model_path = 'model.h5'
if not os.path.exists(model_path):
    model_path = 'workspace/model.h5'

# Check if model.h5 exists FIRST, before loading any heavy libraries  
if not os.path.exists(model_path) or not os.path.isfile(model_path):
    print("\n" + "="*60)
    print("ERROR: model.h5 not found!")
    print("="*60)
    print("Please train the model first by running:")
    print("  docker-compose run --rm fsd-simulation python trainingSimulation.py")
    print("\nOr provide a trained model.h5 file in the project directory.")
    print("="*60 + "\n")
    sys.exit(1)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs
import socketio
import eventlet
import numpy as np
from flask import Flask
from tensorflow.keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
import cv2

sio = socketio.Server()
app = Flask(__name__)
maxSpeed = 50

def preProcess(img):
    img = img[60:135,:,:]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img/255
    return img

@sio.on('telemetry')
def telemetry(sid, data):
    speed = float(data['speed'])
    image = Image.open(BytesIO(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = preProcess(image)
    image = np.array([image])
    steering = float(model.predict(image))
    throttle = 1.0 - speed / maxSpeed
    print('{} {} {}'.format(steering, throttle, speed))
    sendControl(steering, throttle)

@sio.on('connect')
def connect(sid, environ):
    print('Connected')
    sendControl(0, 0)

def sendControl(steering, throttle):
    sio.emit('steer', data={
        'steering_angle': steering.__str__(),
        'throttle': throttle.__str__()
    })

if __name__ == '__main__':
    model = load_model(model_path)  # Load model from detected path
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)