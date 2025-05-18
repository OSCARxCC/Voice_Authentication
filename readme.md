
## 環境
1. OS:Windows10
2. 主要環境:WSL2 (Distribution: Ubuntu20.04)
3. 執行環境: Python虛擬環境
4. Python版本:3.8.10

## Docker安裝 (Downloads for AMD Windows)
- 下載Docker Desktop:https://www.docker.com/products/docker-desktop/
- 打開Docker Desktop進到Setting->Resources->WSL Integration-->
Enable intgration with additional distros-->開啟選項-->Apply & Restart"


##  安裝必要函式庫

### 1. 安裝需求套件 (建議自行建置Python虛擬環境並安裝，避免版本衝突!!)
```bash
pip install -r requirements.txt
```

### 2. 安裝whisper(安裝至少40分鐘 QQ)
```bash
pip install git+https://github.com/openai/whisper.git
```
### 強制安裝在虛擬環境 (請參照當前檔案路徑!!)
```bash
/mnt/e/Code/voice_auth/my_venv/bin/pip install git+https://github.com/openai/whisper.git
```

### 3. 啟動 Mosquitto MQTT broker
```bash
docker run -it -p 1883:1883 eclipse-mosquitto
```


##  執行方式總結
### 1. 於Windows CMD或PowerShell Terminal中啟動 Mosquitto MQTT broker
```bash
docker run -it -p 1883:1883 eclipse-mosquitto
```


### docker啟動若出問題 (路徑請參照自己config的路徑!!)
```
docker run -it -p 1883:1883 -v E:\Code\voice_auth\mosquitto_conf:/mosquitto/config eclipse-mosquitto

```

### 2. 執行 3 個不同終端機 (都要於Python虛擬環境執行!!)
```bash
# Terminal 1：Server
python server.py

# Terminal 2：MITM 攔截者
python mitm.py

# Terminal 3：Client 傳送者
python client.py
```
### 其他
> `audio/test.wav` 為語音檔案，內容為：  
> 「我叫陳大文，電話 0912123456，我的代碼是 1234」




---


## 優化

- 自訂 `audio/test.wav`（可用手機錄音）
- 加入 GUI、Web 介面或流程圖以增加展示亮點
