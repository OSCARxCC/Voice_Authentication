import json
import re
import paho.mqtt.client as mqtt
from utils.asr import transcribe
from utils.crypto import encrypt

key = b'ThisIsASecretKey'  # 16 bytes AES key

def extract_info(text):
    name_match = re.search(r"(我叫|我是)([\w\u4e00-\u9fa5]{2,4})", text)
    phone_match = re.search(r"(09\d{8})", text)
    code_match = re.search(r"(密碼|代碼)?\s*(\d{4})", text)

    name = name_match.group(2) if name_match else "未擷取"
    phone = phone_match.group(1) if phone_match else "未擷取"
    code = code_match.group(2) if code_match else "未擷取"

    return name, phone, code

def main():
    # 錄音轉文字
    text = transcribe("audio/test.wav")  # 假設你有錄音檔 audio.m4a
    print("🎙️ 語音內容：", text)

    # 擷取資訊
    name, phone, code = extract_info(text)
    print(f"🧾 擷取資訊：姓名={name}, 電話={phone}, 代碼={code}")

    # 加密後封裝成 JSON 並發送
    data = {
        "name": encrypt(name, key),
        "phone": encrypt(phone, key),
        "code": encrypt(code, key)
    }

    client = mqtt.Client() 
    client.connect("localhost", 1883, 60)
    client.publish("secure/data", json.dumps(data))
    print("✅ 已發送加密資料")

if __name__ == "__main__":
    main()
