import mock
import requests

from sprintly.people import People

from mocks import MockResponseValid
from test_helper import SprintlyTestCase


class TestPeople(SprintlyTestCase):
    def setUp(self):
        self._people = People('people', 'api', 1)

    def test_list_users(self):
        with mock.patch.object(requests, 'get') as mock_method:
            data = self._get_test_data('list_users0.json')
            mock_method.return_value = MockResponseValid(data)

            users = self._people.list_users()
            self.assertEqual(3, len(users))

            john = users[0]
            self.assertTrue(john['admin'])
            self.assertEqual('John', john['first_name'])
            self.assertEqual('Doe', john['last_name'])
            self.assertEqual(1, john['id'])
            self.assertEqual('john.doe@gmail.com', john['email'])

            jane = users[1]
            self.assertEqual(2, jane['id'])
            self.assertFalse(jane['admin'])

            tarzan = users[2]
            self.assertEqual(3, tarzan['id'])
            self.assertEqual('', tarzan['last_name'])

    def test_invite_user(self):
        with mock.patch.object(requests, 'post') as mock_method:
            data = self._get_test_data('invite_user0.json')
            mock_method.return_value = MockResponseValid(data)

            john = self._people.invite_user('John', 'Doe',
                    'john.doe@gmail.com', admin=False)
            self.assertFalse(john['admin'])
            self.assertEqual('John', john['first_name'])
            self.assertEqual('Doe', john['last_name'])
            self.assertEqual('john.doe@gmail.com', john['email'])

    def test_get_user(self):
        with mock.patch.object(requests, 'get') as mock_method:
                data = self._get_test_data('get_user0.json')
                mock_method.return_value = MockResponseValid(data)

                john = self._people.get_user(1)

                self.assertFalse(john['admin'])
                self.assertEqual('John', john['first_name'])
                self.assertEqual('Doe', john['last_name'])
                self.assertEqual('john.doe@gmail.com', john['email'])

    def test_delete_user(self):
        with mock.patch.object(requests, 'delete') as mock_method:
                data = self._get_test_data('delete_user0.json')
                mock_method.return_value = MockResponseValid(data)

                john = self._people.delete_user(1)

                self.assertFalse(john['admin'])
                self.assertEqual('John', john['first_name'])
                self.assertEqual('Doe', john['last_name'])
                self.assertEqual('john.doe@gmail.com', john['email'])
