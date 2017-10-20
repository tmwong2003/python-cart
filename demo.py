#!/usr/bin/env python
'''
Created on Oct 19, 2017

@author: twong
'''

import argparse
import pandas as pd

import cart.controller


def cart_to_frame(cart):
    '''
    Convert a raw cart into a printable data frame.

    Args:
        cart: A shopping cart

    Returns
        a tuple of the cart ID, printable frame and the total cart cost
    '''
    uuid = cart['uuid']
    columns = ['Name', 'Description', 'Price per unit', 'Quantity']
    df = pd.DataFrame(columns=columns)
    contents = cart['contents']
    descriptions = cart['descriptions']
    for sku in contents:
        description = descriptions[sku]
        df = df.append(pd.Series(index=columns, data=[description['name'], description['description'], description['price'], contents[sku]]), ignore_index=True)
    cost = sum(df['Price per unit'] * df['Quantity'])
    return uuid, df, cost


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--user',
        type=str,
        default='tmw@tmwong.org',
        help='The e-mail address of the owner of the carts'
    )
    args = parser.parse_args()

    controller = cart.controller.Controller()

    print "##### Show any unpurchased carts for {}...".format(args.user)
    carts = controller.get_carts(args.user)
    for cart in carts:
        uuid, df, cost = cart_to_frame(cart)
        print 'Cart {} for user {} costs {:.2f} and contains:'.format(uuid, args.user, cost)
        print df
    print

    print "##### Start a new cart for {}...".format(args.user)
    print
    # TODO: The ordering system is not build out
    contents = {'205591201309003190_7662246479379859829': 3, '141398737587437883_1354554456861557135': 2}
    new_cart = controller.update_cart(args.user, contents=contents)
    uuid, df, cost = cart_to_frame(new_cart)
    print 'New cart {} for user {} costs ${:.2f} and contains:'.format(uuid, args.user, cost)
    print df
    print

    purchased_cart = controller.checkout_cart(uuid)
    uuid, _, cost = cart_to_frame(new_cart)
    print "##### Purchased cart {} for ${:.2f}".format(uuid, cost)
    print

    print("##### Show purchased carts for {}, which should include the just-purchased cart {}".format(args.user, uuid))
    carts = controller.get_carts(args.user, purchased=True)
    for cart in carts:
        uuid, df, cost = cart_to_frame(cart)
        print 'Cart {} for user {} costs {:.2f} and contains:'.format(uuid, args.user, cost)
        print df
    print

    controller._flush_cart_db()
