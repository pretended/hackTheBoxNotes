import hashlib
import os
from binascii import hexlify, unhexlify
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def deriveKey(passphrase: str, salt: bytes=None) -> [str, bytes]:
    if salt is None:
        salt = os.urandom(8)
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf8"), salt, 1000), salt


def encrypt(passphrase: str, plaintext: str) -> str:
    key, salt = deriveKey(passphrase)
    aes = AESGCM(key)
    iv = os.urandom(12)
    plaintext = plaintext.encode("utf8")
    ciphertext = aes.encrypt(iv, plaintext, None)
    return "%s-%s-%s" % (hexlify(salt).decode("utf8"), hexlify(iv).decode("utf8"), hexlify(ciphertext).decode("utf8"))


def decrypt(passphrase: str, ciphertext: str) -> str:
    salt, iv, ciphertext = map(unhexlify, ciphertext.split("-"))
    key, _ = deriveKey(passphrase, salt)
    aes = AESGCM(key)
    plaintext = aes.decrypt(iv, ciphertext, None)
    return plaintext.decode("utf8")


if __name__ == "__main__":
    ciphertext = encrypt("hello", "world")
    print(ciphertext)
    print(decrypt("hello", ciphertext))
    print(decrypt("hello", "6102677198e41d98-84c95e2d7caf6f2d4ccbfe3c-3093cef35d0dba7a24d37f7d4580b5ad83c154329c"))
