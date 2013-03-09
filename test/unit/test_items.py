from sprintly.errors import SprintlyError
from sprintly.items import Items

from mocks import MockSprintlyResponse
from test_helper import SprintlyTestCase


class TestItems(SprintlyTestCase):
    def setUp(self):
        self._items = Items('user', 'key', 'product')

    def test_get_items_raises_on_wrong_type(self):
        item_type = 'random'
        with self.assertRaises(SprintlyError):
            self._items.get_items(item_type=item_type)

    def test_get_items_raises_on_wrong_status(self):
        item_status = 'random'
        with self.assertRaises(SprintlyError):
            self._items.get_items(item_type='task',
                    item_status=item_status)

    def test_get_items_sends_assigned_to_when_valid(self):
        return_value = MockSprintlyResponse(
                status_code=200,
                reason='OK',
                json={})
        sut = self._mock_session_for(self._items, 'get', return_value)
        self._items.get_items(
                item_type='task',
                item_status='in-progress',
                assigned_to=11)
        expected = {
                'type': 'task',
                'status': 'in-progress',
                'assigned_to': 11}
        actual = sut.call_args_list[0][1]['params']
        self.assertDictEqual(expected, actual)
