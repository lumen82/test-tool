import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def populate_public_key(e, n):
    key = rsa.RSAPublicNumbers(e, n).public_key(default_backend())
    return key

def getPem(e, n):
    key = populate_public_key(e, n)
    pem = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem

