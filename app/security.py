import base64
import os
import json
import bcrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from config import SECRET_KEY


def encrypt_text(text: str) -> str:
    nonce = os.urandom(12)
    aesgcm = AESGCM(SECRET_KEY)
    ciphertext_with_tag = aesgcm.encrypt(nonce, text.encode("utf-8"), None)

    payload = {
        "data": base64.b64encode(ciphertext_with_tag[:-16]).decode("utf-8"),
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "tag": base64.b64encode(ciphertext_with_tag[-16:]).decode("utf-8"),
    }

    return base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")


def decrypt_text(encrypted_text: str) -> str:
    payload_json = base64.b64decode(encrypted_text).decode("utf-8")
    payload = json.loads(payload_json)

    ciphertext = base64.b64decode(payload["data"])
    nonce = base64.b64decode(payload["nonce"])
    tag = base64.b64decode(payload["tag"])

    aesgcm = AESGCM(SECRET_KEY)
    plaintext = aesgcm.decrypt(nonce, ciphertext + tag, None)
    return plaintext.decode("utf-8")


def encrypt_return_data_submit(data: dict) -> dict:
    json_data = json.dumps(data)
    encrypted_text = encrypt_text(json_data)
    decrypted_payload = json.loads(base64.b64decode(encrypted_text).decode())

    return {
        "payload": decrypted_payload["data"],
        "nonce": decrypted_payload["nonce"],
        "tag": decrypted_payload["tag"]
    }

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def decrypt_payload(payload_dict: dict) -> dict:
    encrypted_combined = base64.b64encode(json.dumps({
        "data": payload_dict["payload"],
        "nonce": payload_dict["nonce"],
        "tag": payload_dict["tag"]
    }).encode("utf-8")).decode("utf-8")

    decrypted = decrypt_text(encrypted_combined)
    return json.loads(decrypted)
