"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status


class CounterTest(TestCase):
    """Counter tests"""

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        self.client = app.test_client()

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        # creating a counter
        result = self.client.post('/counters/update')
        # ensure returned successful return code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        # check counter value as baseline
        # result = self.client.get('/counters/update')
        # make a call to update counter we just created
        baselineValue = result.get_json()['update']
        result = self.client.put('/counters/empty')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
        # ensure returned successful return code
        # check counter is one more than baseline we measured in check counter value as baseline
        result = self.client.put('/counters/update')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        updateValue = result.get_json()['update']
        self.assertEqual(baselineValue + 1, updateValue)

    def test_read_counter(self):
        """Read a counter"""
        # creating a counter
        result = self.client.post('/counters/read')
        # ensure returned successful return code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        # read counter
        result = self.client.get('/counters/read')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        # counterValue = result.get_json()['read']
        # self.assertEqual(baselineValue + 1,updateValue)
        result = self.client.get('/counters/empty')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)
