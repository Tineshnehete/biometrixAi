import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decipher(encrypted_data):
    message, vector, key_data = encrypted_data

    # Decode base64-encoded values
    encrypted_bytes = base64.b64decode(message)
    iv = base64.b64decode(vector)
    key = base64.urlsafe_b64decode(key_data + "==")  # Adjust padding for JWK

    # The last 16 bytes of AES-GCM output contain the authentication tag
    ciphertext, tag = encrypted_bytes[:-16], encrypted_bytes[-16:]

    # Setup AES-GCM cipher with IV and authentication tag
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt and decode JSON
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return json.loads(decrypted_data.decode())

