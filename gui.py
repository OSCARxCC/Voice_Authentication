import tkinter as tk
import subprocess
import os

def run_client():
    subprocess.Popen(["python3", "client.py"])

def run_server():
    subprocess.Popen(["python3", "server.py"])

def run_mitm():
    subprocess.Popen(["python3", "mitm.py"])

def open_log(folder):
    path = os.path.abspath(folder)
    os.startfile(path)

root = tk.Tk()
root.title("Voice Authentication Dashboard")
root.geometry("800x600")

font_big = ("Helvetica", 16)

tk.Button(root, text="Run Client (Voice → Encrypt → Send)", font=font_big, command=run_client, height=2, width=40).pack(pady=10)
tk.Button(root, text="Start Server (Decrypt & Verify)", font=font_big, command=run_server, height=2, width=40).pack(pady=10)
tk.Button(root, text="Start MITM Interceptor", font=font_big, command=run_mitm, height=2, width=40).pack(pady=10)

tk.Label(root, text="--- View Logs ---", font=("Helvetica", 14, "bold")).pack(pady=5)
tk.Button(root, text="Open Server Logs", font=font_big, command=lambda: open_log("serverlogs"), width=30).pack(pady=5)
tk.Button(root, text="Open MITM Logs", font=font_big, command=lambda: open_log("mitmlogs"), width=30).pack(pady=5)

root.mainloop()