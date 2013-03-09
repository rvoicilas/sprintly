import json
import mock
import os
import requests
import unittest


class SprintlyTestCase(unittest.TestCase):
    def _get_test_data(self, testfile):
        """Retrieves the test json from the specified file"""
        path = os.path.join(os.path.dirname(__file__), 'fixtures', testfile)
        return json.load(open(path))

    def _build_fake_product(self, product_id, product_name):
        return {
                'admin': False,
                'archived': False,
                'email': {
                    'backlog': 'backlog-{}@items.sprint.ly'.format(product_id),
                    'defects': 'defects-{}@items.sprint.ly'.format(product_id),
                    'stories': 'stories-{}@items.sprint.ly'.format(product_id),
                    'tasks': 'tasks-{}@items.sprint.ly'.format(product_id),
                    'tests': 'tests-{}@items.sprint.ly'.format(product_id)
                    },
                'id': product_id,
                'name': product_name
                }

    def _mock_session_for(self, obj, operation, value):
        session_mock = mock.Mock(return_value=value)
        session = requests.session()
        setattr(session, operation, session_mock)
        setattr(obj, 'session', session)
        return session_mock
