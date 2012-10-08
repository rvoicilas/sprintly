import json
import os
import unittest


class SprintlyTestCase(unittest.TestCase):
    def _get_test_data(self, testfile):
        """Retrieves the test json from the specified file"""
        path = os.path.join(os.path.dirname(__file__), 'fixtures', testfile)
        return json.load(open(path))
