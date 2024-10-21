import unittest
import json
from src.app import app
from src.get_temp_avg import get_temp_avg
from __version__ import VERSION

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_version(self):
        response = self.app.get('/api/version')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"version": VERSION})

    def test_temp_avg(self):
        with open("data/boxes.json", "r", encoding="utf-8") as f:
            boxes = json.load(f)
        self.assertEqual(get_temp_avg(boxes), 16.825714285714287)

    def test_get_temperature(self):
        response = self.app.get('/api/temperature')
        self.assertEqual(response.status_code, 200)