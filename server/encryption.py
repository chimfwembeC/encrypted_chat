# encryption.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

class AESCipher:
    """
    AESCipher uses AES in CBC mode with PKCS7 padding.
    A new random IV is generated for each encryption and is prepended to the ciphertext.
    """
    def __init__(self, key):
        self.key = key
        self.backend = default_backend()
        # AES.block_size is in bits (128 bits)
        self.block_size = algorithms.AES.block_size

    def encrypt(self, plaintext):
        # Generate a random 16-byte IV for each encryption
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(self.block_size).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        # Prepend the IV to the ciphertext so it can be used in decryption
        return iv + ciphertext

    def decrypt(self, ciphertext):
        # Extract the IV from the first 16 bytes
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(self.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext.decode('utf-8')
