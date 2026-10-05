import boto3, os, json, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

kms = boto3.client("kms", region_name="us-east-2")
KEY = "alias/examen-kms"

def b64(x): return base64.b64encode(x).decode()
def unb64(x): return base64.b64decode(x)

def cifrar(mensaje):
    r = kms.generate_data_key(KeyId=KEY, KeySpec="AES_256")
    key, key_cifrada = r["Plaintext"], r["CiphertextBlob"]

    nonce = os.urandom(12)
    mensaje_cifrado = AESGCM(key).encrypt(nonce, mensaje.encode(), None)

    sobre = {
        "key": b64(key_cifrada),
        "nonce": b64(nonce),
        "mensaje": b64(mensaje_cifrado)
    }

    del key
    with open("sobre.json", "w") as f:
        json.dump(sobre, f, indent=2)

def descifrar():
    with open("sobre.json") as f:
        sobre = json.load(f)

    key = kms.decrypt(CiphertextBlob=unb64(sobre["key"]))["Plaintext"]
    mensaje = AESGCM(key).decrypt(
        unb64(sobre["nonce"]), unb64(sobre["mensaje"]), None
    )
    del key
    return mensaje.decode()

mensaje = "Mensaje secreto para el examen de AWS KMS"
cifrar(mensaje)
print("Sobre digital creado: sobre.json")
print("Mensaje descifrado:", descifrar())
