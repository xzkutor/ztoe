import unittest
import asyncio
from unittest.mock import patch, AsyncMock
from ztoe.schedule import Schedule, isElectricityPlanned

class TestSchedule(unittest.TestCase):

    def setUp(self):
        with open('test.html', 'r', encoding='cp1251') as file:
            self.html = file.read()
        self.schedule = Schedule(self.html)

    @patch('ztoe.schedule.Schedule.get_all', new_callable=AsyncMock)
    def test_get_all(self, mock_get_all):
        mock_get_all.return_value = [
            {"sector": 1, "queue": 1, "data": {0: {"time": "08:00", "electricity": True}}},
            {"sector": 2, "queue": 2, "data": {0: {"time": "09:00", "electricity": False}}}
        ]
        result = asyncio.run(self.schedule.get_all())
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

    @patch('ztoe.schedule.Schedule.get_all', new_callable=AsyncMock)
    def test_get_queue(self, mock_get_all):
        mock_get_all.return_value = [
            {"sector": 1, "queue": 1, "data": {0: {"time": "08:00", "electricity": True}}},
            {"sector": 2, "queue": 2, "data": {0: {"time": "09:00", "electricity": False}}}
        ]
        self.schedule._schedule=mock_get_all.return_value
        result = asyncio.run(self.schedule.get_queue(1))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["queue"], 1)

    @patch('ztoe.schedule.Schedule.get_all', new_callable=AsyncMock)
    def test_get_sector(self, mock_get_all):
        mock_get_all.return_value = [
            {"sector": 1, "queue": 1, "data": {0: {"time": "08:00", "electricity": True}}},
            {"sector": 2, "queue": 2, "data": {0: {"time": "09:00", "electricity": False}}}
        ]
        self.schedule._schedule = mock_get_all.return_value
        result = asyncio.run(self.schedule.get_sector(1))
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["sector"], 1)

    def test_isElectricityPlanned(self):
        self.assertTrue(isElectricityPlanned("#ffffff"))
        self.assertFalse(isElectricityPlanned("#000000"))

if __name__ == '__main__':
    unittest.main()