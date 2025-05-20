import json
import paho.mqtt.client as mqtt
from utils.crypto import decrypt, checksum
import datetime
import os

def get_windows_host_ip():
    with open("/etc/resolv.conf", "r") as f:
        for line in f:
            if "nameserver" in line:
                return line.strip().split()[1]

os.makedirs("serverlogs", exist_ok=True)

def log_server_verification(result, expected=None, actual=None, reason=None, uuid=None):
    with open("serverlogs/server_log.json", "a", encoding="utf-8") as f:
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "result": result
        }
        if uuid:
            entry["uuid"] = uuid
        if expected:
            entry["expected"] = expected
        if actual:
            entry["actual"] = actual
        if reason:
            entry["reason"] = reason
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

key = b'ThisIsASecretKey'

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    with open("database.json", encoding='utf-8') as f:
        db = json.load(f)
    uuid_val = payload.get("uuid")
    try:
        name = decrypt(payload["name"], key)
        phone = decrypt(payload["phone"], key)
        code = decrypt(payload["code"], key)
        combined = name + phone + code
        local_checksum = checksum(combined)
        incoming_checksum = payload.get("checksum")

        print(f"[伺服器接收 UUID={uuid_val}] 解密結果: {name}, {phone}, {code}")

        if local_checksum != incoming_checksum:
            print("❌ 驗證失敗：checksum 不符")
            log_server_verification("checksum 錯誤", uuid=uuid_val, expected=local_checksum, actual=incoming_checksum)
            return

        if name == db["name"] and phone == db["phone"] and code == db["code"]:
            print("身份驗證成功!!!")
            log_server_verification("驗證成功", expected=db, actual={"name": name, "phone": phone, "code": code}, uuid=uuid_val)
        else:
            print("驗證失敗(x)")
            print("預期資料:", db)
            print("實際資料:", {"name": name, "phone": phone, "code": code})
            log_server_verification("驗證失敗", expected=db, actual={"name": name, "phone": phone, "code": code}, uuid=uuid_val)
    except Exception as e:
        print("解密失敗或資料被竄改:", e)
        log_server_verification("解密錯誤", reason=str(e), uuid=uuid_val)
        # log_server_verification("驗證失敗", expected=db, actual={"name": name, "phone": phone, "code": code}, uuid=uuid_val)

server = mqtt.Client()
server.on_message = on_message
server.connect(get_windows_host_ip(), 1883, 60)
server.subscribe("forward/data")
print("Server 正在等待資料...")
server.loop_forever()