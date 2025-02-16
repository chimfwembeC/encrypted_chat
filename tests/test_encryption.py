import unittest
from client.encryption import AESCipher
import os

class TestEncryption(unittest.TestCase):
    def setUp(self):
        self.key = os.urandom(32)
        self.cipher = AESCipher(self.key)
    
    def test_encryption_decryption(self):
        plaintext = "Hello, World!"
        encrypted = self.cipher.encrypt(plaintext)
        decrypted = self.cipher.decrypt(encrypted)
        self.assertEqual(plaintext, decrypted)

if __name__ == "__main__":
    unittest.main()