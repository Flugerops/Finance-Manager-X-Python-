import unittest
from datetime import datetime
from fastapi.testclient import TestClient
from main import app

# I can`t make a tests for get requests so only posts :(


class TestBackend(unittest.TestCase):

    def setUp(self) -> None:
        self.app = TestClient(app)

    def test_reg_user(self):
        response = self.app.post("/user_reg", json={"owner": "test"})
        self.assertEqual(response.status_code, 200)

    def test_add_income(self):
        data = {
            "owner": "test",
            "amount": 15.0,
            "category": "work"
        }
        response = self.app.post("/change_balance", json=data)
        self.assertEqual(response.status_code, 200)

    def test_filters(self):
        data = {
            "owner": "test",
            "start_date": "2024-08-09",
            "end_date": "2024-08-09"
        }
        response = self.app.post("/filters", json=data)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
