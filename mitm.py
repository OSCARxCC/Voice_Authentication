import paho.mqtt.client as mqtt
import json
import base64
import datetime
import os
import requests

os.makedirs("mitmlogs", exist_ok=True)

FLASK_SERVER = "http://localhost:5000/emit"

# 儲存紀錄
def log_to_file(original, modified=None):
    with open("mitmlogs/mitm_log.json", "a", encoding="utf-8") as f:
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "original": original
        }
        if modified:
            entry["modified"] = modified
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# MQTT 訊息處理

def on_message(client, userdata, msg):
    incoming = json.loads(msg.payload.decode())
    data = incoming["data"]
    mitm_enabled = incoming.get("mitm", False)

    uuid_val = data.get("uuid", "(無 UUID)")
    print(f"⚠️ MITM 攔截 UUID={uuid_val}：", json.dumps(data, ensure_ascii=False))

    # 回推攔截密文
    requests.post(FLASK_SERVER, json={"mitmIntercept": data})

    modified_data = data.copy()
    if mitm_enabled:
        original_code = data['code']['ciphertext']
        modified_data['code']['ciphertext'] = base64.b64encode(b"0000HACKED").decode()
        print(f"⚠️ 已竄改 code.ciphertext：{original_code} → {modified_data['code']['ciphertext']}")

        # 回推竄改後密文
        requests.post(FLASK_SERVER, json={"mitmTampered": modified_data})

    log_to_file(original=data, modified=modified_data if mitm_enabled else None)
    mitm.publish("forward/data", json.dumps(modified_data))

# 建立連線
mitm = mqtt.Client()
mitm.on_message = on_message
mitm.connect("localhost", 1883, 60)
mitm.subscribe("secure/data")
print("🧑‍💻 MITM 正在攔截資料...")
mitm.loop_forever()