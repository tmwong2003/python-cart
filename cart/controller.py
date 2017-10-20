'''
Created on Oct 19, 2017

@author: tmwong
'''

import cart_db
import catalog_db


class Controller(object):
    '''
    classdocs
    '''

    def __init__(self):
        self._cart_db = cart_db.CartDb()
        self._catalog_db = catalog_db.CatalogDb()

    def _populate_cart(self, cart):
        '''Populate a cart with the descriptions corresponding to each SKU
        in the cart contents.

        Args:
            cart: A cart database record

        Returns:
            a dict-like containing the original cart contents annotated
            with the descriptions corresponding to each SKU
        '''
        # The keys of the cart contents should be a list of SKUs.
        descriptions = self._catalog_db.get_descriptions(cart.contents.keys())
        populated_cart = {
            'uuid': cart.name,
            'contents': cart.contents,
            'descriptions': descriptions,
            'purchased': cart.purchased,
        }
        return populated_cart

    def get_carts(self, user, purchased=False):
        '''Get all carts for a user.

        Args:
            user: The user name
            purchased: A boolean to select whether to return purchased carts
                or unpurchased carts
        '''
        carts = self._cart_db.find(user, purchased=purchased)
        populated_carts = []
        for i in carts.index:
            # Select descriptions from catalog DB where SKUs; compute cost
            populated_cart = self._populate_cart(carts.loc[i])
            populated_carts.append(populated_cart)
        return populated_carts

    def update_cart(self, user, uuid=None, contents=None):
        '''
        Update the contents of a shopping cart.

        Args:
            user: The user name
            uuid: The unique ID of the cart. If `None`, create a new cart.
            contents: A map of SKUs to quantities representing the contents
                of the cart.

        Returns:
            the populated cart
        '''
        try:
            cart = self._cart_db.update(user, uuid, contents)
        except ValueError:
            print "ERROR: Cannot change the contents of a purchased cart"
        return self._populate_cart(cart)

    def checkout_cart(self, uuid, payment_info=None):  # @UnusedVariable
        '''
        Check out with the contents of a cart

        Args:
            uuid: The unique ID of the cart
            payment_info: A string blob of payment information (unused)

        Returns:
            the checked-out cart
        '''
        try:
            cart = self._cart_db.purchase(uuid)
            # Next steps:
            # 1. Compute the total cart cost.
            # 2. Send the cost and payment info to the payment system.
            # 3. Send the cart to the shipping system
        except ValueError:
            print "ERROR: Cannot change the contents of a purchased cart"
        except Exception:
            # If anything fails during the checkout, "unpurchase" the
            # cart. This may involve send the total cost to the payment
            # system for a refund.
            self._cart_db.unpurchase(uuid)
            raise RuntimeError('ERROR: Unable to purchase cart contents')
        return cart

    def _flush_cart_db(self):
        '''
        Flush the cart database to stable storage.
        '''
        self._cart_db._flush()
