from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from utils.asr import transcribe
from utils.crypto import encrypt, checksum
import uuid
import os
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/simulate", methods=["POST"])
def simulate_audio():
    audio_path = "audio/test.wav"
    if not os.path.exists(audio_path):
        return jsonify({"error": "test.wav 不存在"}), 404

    transcript = transcribe(audio_path)
    name, phone, code = extract_info(transcript)
    combined = name + phone + code

    key = b'ThisIsASecretKey'
    packet = {
        "uuid": str(uuid.uuid4()),
        "name": encrypt(name, key),
        "phone": encrypt(phone, key),
        "code": encrypt(code, key),
        "checksum": checksum(combined)
    }

    # 前端決定是否開啟 MITM
    try:
        mitm = request.json.get("mitm", False)
    except:
        mitm = False

    # 推播 client 發送封包
    socketio.emit("message", json.dumps({"clientData": packet}))

    # 發送 MQTT 封包
    mqtt_client.publish("secure/data", json.dumps({"data": packet, "mitm": mitm}))

    return jsonify({"transcript": transcript})

@app.route("/emit", methods=["POST"])
def external_emit():
    content = request.json
    socketio.emit("message", json.dumps(content))
    return "ok"

@socketio.on("connect")
def test_connect():
    print("Client connected")

@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected")

def extract_info(text):
    import re
    name_match = re.search(r"(\u6211\u53eb|\u6211\u662f)([\w\u4e00-\u9fa5]{2,4})", text)
    phone_match = re.search(r"(09\d{8})", text)
    code_match = re.search(r"(\u4ee3\u78bc|\u5bc6\u78bc)[\u662f\u70ba:]?\s*(\d{4})", text)
    name = name_match.group(2) if name_match else "未擷取"
    phone = phone_match.group(1) if phone_match else "未擷取"
    code = code_match.group(2) if code_match else "未擷取"
    return name, phone, code

if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    socketio.run(app, host="0.0.0.0", port=5000)