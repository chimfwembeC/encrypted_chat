import unittest
from client.client import authenticate

class TestClient(unittest.TestCase):
    def test_authenticate(self):
        self.assertTrue(authenticate("user1", "password1"))
        self.assertFalse(authenticate("user1", "wrongpassword"))

if __name__ == "__main__":
    unittest.main()