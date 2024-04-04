import unittest

from fastapi import status
from fastapi.testclient import TestClient

from main import app


class TestCustomerEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_list(self):
        url = "/v1/customers/List"
        response = self.client.get(url)

        body = response.json().get("body")
        expected_keys = ["customers"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(body.keys()), expected_keys)
