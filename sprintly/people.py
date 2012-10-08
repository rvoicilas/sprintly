from api import Api

"""
people.py
~~~~~~~~~

This module implements sprintly's people API.
"""


class People(Api):
    # template of urls

    def __init__(self, user, key, product_id):
        super(People, self).__init__(user, key)
        self._product_id = product_id

        self._urls = \
                dict(people='https://sprint.ly/api/products/%s/people.json' %
                        self._product_id)

    def list_users(self):
        """Returns a list of users records that are members of self._product_id"""
        return self._make_get_request(self._urls['people'])

    def invite_user(self, first_name, last_name, email, admin=False):
        """Invite someone to the product - it sends an email to the address
        specified in the request.

        The user making this API request must be an admin of the product or
        the account holder who created the product.

        :param first_name: String. Their first name.
        :param last_name: String. Their last name.
        :param email: String. The email address where the invite is sent.
        :param admin: Boolean. Whether this person is going to be an admin
        of the product. Defaults to False.
        """
        # FIXME: Make sure that admin gets passed in as True/False and not as
        # y/n
        data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'admin': admin
                }
        return self._make_post_request(self._urls['people'], data=data)

    def get_user(self, user_id):
        """Return the record for the provided user_id.

        :param user_id: Integer. The id of the user to be returned.
        """
        url = 'https://sprint.ly/api/products/%s/people/%s.json' %\
                (self._product_id, user_id)
        return self._make_get_request(url)

    def delete_user(self, user_id):
        """Remove the given user from the product.

        The user making this API request must be an admin of the product or
        the account holder who created the product.

        :param user_id: Integer. The id of the user that will be deleted.
        """
        url = 'https://sprint.ly/api/products/%s/people/%s.json' %\
                (self._product_id, user_id)
        return self._make_delete_request(url)
