from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib
import uuid

def pad(text):
    while len(text) % 16 != 0:
        text += ' '
    return text

def checksum(data_str):
    return hashlib.sha256(data_str.encode()).hexdigest()

def encrypt(text, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(pad(text).encode())
    return {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }

def decrypt(enc_data, key):
    nonce = base64.b64decode(enc_data['nonce'])
    ciphertext = base64.b64decode(enc_data['ciphertext'])
    tag = base64.b64decode(enc_data['tag'])
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode().strip()