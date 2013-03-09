import mock
import requests

from sprintly.errors import SprintlyUnauthorizedError
from sprintly.products import Products

from mocks import MockSprintlyResponse
from test_helper import SprintlyTestCase


class TestProducts(SprintlyTestCase):
    def setUp(self):
        self._products = Products('products', 'api')


    def _mock_products_session(self, operation, value):
        session_mock = mock.Mock(return_value=value)
        session = requests.session()
        setattr(session, operation, session_mock)
        self._products.session = session

    def test_add_product_raises_when_no_paying_account(self):
        return_value = MockSprintlyResponse(
                status_code=403,
                reason='FORBIDDEN',
                json={'code': 403, 'message': 'You do not own an account.'})

        self._mock_products_session('post', return_value)

        with self.assertRaises(SprintlyUnauthorizedError) as cm:
            self._products.add_product('new-sprintly-product')
        self.assertEqual('403 - FORBIDDEN', cm.exception.message)

    def test_add_product_ok(self):
        product_name = 'shinny-new-product'
        return_value = MockSprintlyResponse(
                status_code=200,
                reason='OK',
                json={
                    'admin': True,
                    'archived': False,
                    'id': 3,
                    'name': product_name
                    }
                )
        self._mock_products_session('post', return_value)
        self.assertDictEqual(return_value.json,
                self._products.add_product(product_name))

    def test_add_products_makes_list_unique(self):
        add = mock.Mock()
        self._products.add_product = add
        self._products.add_products(['one', 'one'])
        add.assert_called_once_with('one')

    def test_get_product(self):
        product = self._build_fake_product(222, 'whales!')
        return_value = MockSprintlyResponse(
                status_code=200,
                reason='OK',
                json=product)
        self._mock_products_session('get', return_value)
        self.assertDictEqual(product, self._products.get_product(222))

    def test_list_products(self):
        products = [self._build_fake_product(111256, 'dolphines!')]
        return_value = MockSprintlyResponse(
                status_code=200,
                reason='OK',
                json=products)
        self._mock_products_session('get', return_value)
        self.assertEqual(products, self._products.list_products())

    def test_delete_product_no_paying_account(self):
        return_value = MockSprintlyResponse(
                status_code=403,
                reason='FORBIDDEN',
                json={'code': 403, 'message': 'You do not own an account.'})
        self._mock_products_session('delete', return_value)

        with self.assertRaises(SprintlyUnauthorizedError) as cm:
            self._products.delete_product(333)
        self.assertEqual('403 - FORBIDDEN', cm.exception.message)

    def test_delete_product_ok(self):
        product_name = 'drop-this'
        return_value = MockSprintlyResponse(
                status_code=200,
                reason='OK',
                json={
                    'admin': True,
                    'archived': False,
                    'id': 3,
                    'name': product_name
                    }
                )
        self._mock_products_session('delete', return_value)
        self.assertDictEqual(return_value.json,
                self._products.delete_product(product_name))
