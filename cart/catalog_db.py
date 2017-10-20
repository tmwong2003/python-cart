'''
Created on Oct 19, 2017

@author: twong
'''

import os
import pandas as pd

MODULE_DIRNAME = os.path.dirname(__file__)


class CatalogDb(object):
    CATALOG_DB_FILE = os.path.join(MODULE_DIRNAME, 'catalog_db.csv')

    '''
    The catalog database is indexed by SKU. For each SKU, we have entries
    for the item name, item price, and item description.
    '''
    CATALOG_DB_COLUMNS = ['name', 'price', 'description']

    def __init__(self):
        '''
        Create a cart database object. We represent the database as a
        pandas table for simplicity; in practice, we would want an actual
        database backend.
        '''
        if os.path.exists(self.CATALOG_DB_FILE):
            self._db = pd.read_csv(self.CATALOG_DB_FILE, index_col=0)
        else:
            raise RuntimeError('Missing catalog file {}'.format(self.CATALOG_DB_FILE))
        if sorted(self.CATALOG_DB_COLUMNS) != sorted(self._db.columns.values):
            return
            raise RuntimeError(
                'Got possibly malformed catalog file {}: Expected columns {}, got {}'.format(
                    self.CATALOG_DB_FILE,
                    self.CATALOG_DB_COLUMNS,
                    self._db.columns,
                )
            )

    def get_descriptions(self, skus):
        '''
        Get descriptions corresponding to a list of SKUs.

        Args:
            skus: A list of SKUs

        Returns:
            A map of SKUs to corresponding dicts containing item
                descriptions
        '''
        return self._db.loc[skus].to_dict(orient='index')
