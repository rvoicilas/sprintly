import mock
import requests

from sprintly.errors import SprintlyUnauthorizedException
from sprintly.products import Products

from mocks import MockResponseUnauthorized, MockResponseValid
from test_helper import SprintlyTestCase


class TestProducts(SprintlyTestCase):
    def setUp(self):
        self._products = Products('products', 'api')

    def test_add_products_returns_products(self):
        self._products.add_product = lambda product: {
                'admin': 'true',
                'archived': False,
                'id': 0,
                'name': product}
        expected_product_names = ['sprint.ly', 'sprint.py']
        products = [p['name'] for p in
                    self._products.add_products(expected_product_names)]
        self.assertEqual(len(expected_product_names), len(products))
        for product in expected_product_names:
            self.assertIn(product, products)

    def test_add_products_makes_list_unique(self):
        self._products.add_product = lambda product: {}
        products = self._products.add_products(['one', 'one'])
        self.assertEqual(1, len(products))

    def test_add_product_raises_when_unauthorized(self):
        with mock.patch.object(requests, 'post') as mock_method:
            mock_method.return_value = MockResponseUnauthorized

            with self.assertRaises(SprintlyUnauthorizedException):
                self._products.add_product('new-sprintly-product')

            self.assertEqual(1, mock_method.call_count)

    def test_update_product_raises_when_unauthorized(self):
        with mock.patch.object(requests, 'post') as mock_method:
            mock_method.return_value = MockResponseUnauthorized

            with self.assertRaises(SprintlyUnauthorizedException):
                self._products.update_product(1, 'sprintly',
                        archived=True)

            self.assertEqual(1, mock_method.call_count)

    def test_update_product_archived_properly_converted(self):
        with mock.patch.object(requests, 'post') as mock_method:
            self._products.update_product(1, 'sprintly', archived=True)
            expected = {'data': {'archived': 'y', 'name': 'sprintly'}}
            self.assertEqual(expected, mock_method.call_args[1])

    def test_delete_product_raises_when_unauthorized(self):
        with mock.patch.object(requests, 'delete') as mock_method:
            mock_method.return_value = MockResponseUnauthorized

            with self.assertRaises(SprintlyUnauthorizedException):
                self._products.delete_product(1)

            self.assertEqual(1, mock_method.call_count)

    def test_delete_product_returns_product_record(self):
        """Based only on the documentation, the account used for these
        tests didn't have enough privileges.
        """
        with mock.patch.object(requests, 'delete') as mock_method:
            data = self._get_test_data('delete_product0.json')
            mock_method.return_value = MockResponseValid(data)

            record = self._products.delete_product(12)

            self.assertTrue(record['admin'])
            self.assertFalse(record['archived'])
            self.assertEqual('sprintly', record['name'])
            self.assertEqual(12, record['id'])

    def test_list_products(self):
        with mock.patch.object(requests, 'get') as mock_method:
            data = self._get_test_data('list_products0.json')
            mock_method.return_value = MockResponseValid(data)

            products = self._products.list_products()
            self.assertEqual(1, len(products))

            product = products[0]
            expected_keys = ['id', 'name', 'admin', 'created_at',
                    'archived', 'email']
            for key in product:
                self.assertIn(key, expected_keys)
