'''
Created on Oct 19, 2017

@author: tmwong
'''

import os
import pandas as pd
import uuid as cart_uuid

MODULE_DIRNAME = os.path.dirname(__file__)


class CartDb(object):
    CART_DB_FILE = os.path.join(MODULE_DIRNAME, 'cart_db.pickle')

    '''
    The cart database is indexed by cart universal unique ID. For each
    cart, we have entries for the user (i.e., the cart owner), the contents
    (a map of SKU to desired quantity for each SKU), and a flag to indicate
    if the owner has or has not purchased the cart contents.
    '''
    CART_DB_COLUMNS = ['user', 'contents', 'purchased']

    def __init__(self):
        '''
        Create a cart database object. We represent the database as a
        pandas table for simplicity; in practice, we would want an actual
        database backend.
        '''
        if os.path.exists(self.CART_DB_FILE):
            self._db = pd.read_pickle(self.CART_DB_FILE)
        else:
            self._db = pd.DataFrame(columns=self.CART_DB_COLUMNS)

    def _flush(self):
        '''
        Flush the cart database to stable storage. Required for the
        prototype because the "database" is actually an in-memory pandas
        dataframe.
        '''
        self._db.to_pickle(self.CART_DB_FILE)

    def create(self, user):
        '''
        Create a new shopping cart for the named user, and return the
        new cart database record.
        '''
        uuid = str(cart_uuid.uuid4())
        self._db = self._db.append(pd.Series(name=uuid, index=self.CART_DB_COLUMNS, data=[user, {}, False]))
        return uuid

    def find(self, user, purchased=False):
        '''
        Find all shopping carts for the named user, and return the
        cart database records. Optionally, restrict the search by whether
        or not the user has purchased a particular cart.
        '''
        results = self._db[(self._db.user == user) & (self._db.purchased == purchased)]
        return results

    def update(self, user, uuid, contents):
        '''
        Update the contents of a shopping cart

        Args:
            uuid: The unique ID of the cart.
            contents: A map of SKUs to desired quantity for each SKU; note
                that this *overwrites* the existing contents in the cart
                record. We drop any SKUs with zero quantities before
                updating the record.

        Returns:
            the updated cart database record

        Raises:
            ValueError: If the uuid specifies a previouslu purchased cart.
        '''
        if uuid is None:
            uuid = self.create(user)
        if uuid in self._db.index and self._db.loc[uuid].purchased:
            raise ValueError('UUID specifies a purchased cart')
        contents = dict([(sku, contents[sku]) for sku in contents if contents[sku] > 0])
        self._db.loc[uuid].contents = contents
        return self._db.loc[uuid]

    def purchase(self, uuid):
        '''Mark a shopping cart as purchased, which locks the cart from
        future updates.

        Args:
            uuid: The unique ID of the cart.

        Returns:
            the purchased cart database record

        Raises:
            ValueError: If the uuid specifies a previously purchased cart.
        '''
        if not self._db.loc[uuid].purchased:
            self._db.loc[uuid].purchased = True
            return self._db.loc[uuid]
        else:
            raise ValueError('UUID specifies a purchased cart')

    def unpurchase(self, uuid):
        '''Mark a shopping cart as unpurchased, which unlocks the cart to
        allow future updates.

        Args:
            uuid: The unique ID of the cart.
        '''
        self._db.at[uuid].purchased = False
