import GenerateKey
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64

def getEncodeInfo(msg, e, n):
    rsaKey = RSA.importKey(GenerateKey.getPem(e, n))
    cipher = Cipher_pkcs1_v1_5.new(rsaKey)
    cipher_text = base64.b64encode(cipher.encrypt(msg.encode(encoding="utf-8")))
    cipher_text = cipher_text.decode("utf-8")
    print(cipher_text)
    return cipher_text
