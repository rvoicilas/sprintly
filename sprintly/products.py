from api import Api

"""
products.py
~~~~~~~~~~~~

This module implements sprintlys' products API.
"""


class Products(Api):
    # templates of urls
    _urls = dict(products='https://sprint.ly/api/products.json',
                 product='https://sprint.ly/api/products/%s.json')

    def list_products(self):
        """Returns all of the products the user is a member of."""
        return self._make_get_request(self._urls['products'])

    def add_product(self, product):
        """Creates new product. Returns the product record
        that was just created. It can raise 403 when the user accessing this
        endpoint doesn't have a paying account.

        :param product: String. The name of the product to create.
        """
        return self._make_post_request(self._urls['products'],
                                       data=dict(name=product))

    def add_products(self, products):
        """Adds new products. Returns a list of newly added products.

        :param products: List of product names.
        """
        return [self.add_product(product) for product in set(products)]

    def get_product(self, product_id=None):
        """Returns a single product identified by :param product_id.

        :param product_id: Integer. The id of the product you want to retrieve.
        """
        return self._make_get_request(self._urls['product'] % product_id)

    def update_product(self, product_id, name, archived=False):
        """Allows you to update the name of the product. This endpoint can also
        be used to archive or unarchive a product.

        :param product_id: Integer. The product id that needs to be updated.
        :param name: String. The name of the product (old or new).
        :param archived: Boolean. Defaults to False.
        """
        archived = 'y' if archived else 'n'
        return self._make_post_request(self._urls['product'] % product_id,
                                       data=dict(name=name, archived=archived))

    def delete_product(self, product_id):
        """Mark the product as archived. Returns the product record of the
        product you are archiving. Works only if you have a paying account;
        otherwise it raises a 403 HTTP error.

        :param product_id: Integer. The product id that needs to be archived.
        """
        return self._make_delete_request(self._urls['product'] % product_id)
