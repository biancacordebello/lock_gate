from flask import Flask, render_template, request, redirect, url_for
import cv2
import face_recognition_models
import face_recognition
import numpy as np
import os

app = Flask(__name__)

registered_face_image_path = 'static/Image2.jpg'
known_face_encoding = None

def load_registered_face():
    global known_face_encoding
    if os.path.exists(registered_face_image_path):
        image = face_recognition.load_image_file(registered_face_image_path)
        known_face_encoding = face_recognition.face_encodings(image)[0]

def is_person_registered(captured_face_encoding):
    if known_face_encoding is not None:
        results = face_recognition.compare_faces([known_face_encoding], captured_face_encoding)
        return results[0]
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    video_capture.release()

    if not ret:
        return "Erro ao capturar a imagem da câmera."

    # Verifica se a imagem foi capturada corretamente
    if frame is None:
        return "Nenhuma imagem capturada."

    # Converta a imagem para RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Usando cv2 para conversão

    # Detecta os locais e codificações dos rostos
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if len(face_encodings) == 0:
        return "Nenhum rosto detectado na imagem."

    captured_face_encoding = face_encodings[0]
    if is_person_registered(captured_face_encoding):
        message = "Passagem liberada."
    else:
        message = "Passagem bloqueada."

    # Salvar imagem capturada
    image_path = 'static/captured_face.jpg'
    cv2.imwrite(image_path, frame)

    return render_template('result.html', message=message, image_path=image_path)

if __name__ == '__main__':
    load_registered_face()
    app.run(debug=True)
