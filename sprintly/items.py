from api import Api
from errors import SprintlyError

"""
items.py
~~~~~~~~

Implements sprintlys' items API.
"""


class Items(Api):
    _ITEMS_URL = 'https://sprint.ly/api/products/{0}/items.json'

    _VALID_ITEM_TYPES = ('story', 'task', 'defect', 'test')

    _VALID_ITEM_STATUSES = ('backlog', 'in-progress', 'completed', 'accepted')

    def __init__(self, user, key, product_id, *args, **kwargs):
        self._product_id = product_id
        super(Items, self).__init__(user, key, *args, **kwargs)

    def get_items(self, item_type=None, item_status=None,
            assigned_to=None, **kwargs):

        if item_type not in self._VALID_ITEM_TYPES:
            raise SprintlyError(("Item type '{0}' is not a valid value. "
                "Consider '{1}' as values.").format(item_type,
                    ', '.join(self._VALID_ITEM_TYPES)))

        if item_status not in self._VALID_ITEM_STATUSES:
            raise SprintlyError(("Item status '{0}' is not a valid value. "
                "Consider '{1}' as statuses.").format(item_status,
                    ', '.join(self._VALID_ITEM_STATUSES)))

        url = self._ITEMS_URL.format(self._product_id)

        kwargs = {
                'type': item_type,
                'status': item_status}

        if assigned_to is not None:
            kwargs['assigned_to'] = assigned_to

        return self._make_get_request(url, params=kwargs)
