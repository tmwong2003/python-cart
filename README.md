# python-cart

`python-cart` is an implementation of a simple Python web store and shopping cart back-end architecture.

## Architecture description

A simple back-end architecture comprises the following set of independent services:

1. A catalog database (catalog DB) that serves up descriptions of items available for sale.

1. A cart database (cart DB) that manages shopping cart contents between client web sessions. Each cart has a unique cart ID, a user name identifying a client that owns the cart, and a short table of the cart contents.

1. An identity provider (IDP) that manages client authentication.

1. A payment processor that charges the client once they have decided to check out with a particular cart full of items.

1. A controller service (controller) that processes incoming client requests and prepares the responses used to render the web interface on the client user agent.

The typical control flow (assuming no error conditions) during a session would be as follows:

1. A client contacts the controller.

1. The controller redirects the client to the IDP to complete an authentication process and obtain authentication credentials. The cart DB uses these credentials to identify the client as the owner of one or more carts.

1. The controller contacts that catalog DB to retrieve the items available for sale.

1. The controller contacts the cart DB to retrieve any outstanding unpurchased carts owned by the client.

1. The controller presents items the available for sale and the unpurchased carts to the client.

1. The client browses through the presented items, and optionally submits zero or more cart updates during the session. The client may update an existing cart, or create a new cart.

1. Upon receiving an update, the controller saves the update at the cart DB.

1. Eventually, the client optionally submits a checkout request for a cart along with payment information.

1. Upon receiving a checkout, the controller marks the cart as purchased at the cart DB, forwards the payment information to the payment processor. If the payment processor throws an exception, the controller unmarks the cart as purchased (or “marks the cart as unpurchased”).

## Basic cart demonstration implementation

`python-cart` implements a Python demonstration of the catalog DB, cart, DB, and controller service. The demo runs under Python 2.7, and requires installation of the `pandas` data analysis library. The Python module and class hierarchy follows directly from the architecture as described in the previous section, but for the time being omits the IDP and payment processor. Important implementation classes include:

- `cart.catalog_db.CatalogDb`: A Python API to the catalog DB. `CatalogDb` provides a `get_description()` method to return a list of item descriptions corresponding to zero or more SKUs. Internally, `CatalogDb` uses a pandas dataframe backed by the file `cart/catalog_db.csv` to hold a table of descriptions indexed by SKU, but one could replace the dataframe with accesses to an underlying database server.

- `cart.cart_db.CartDb`: A Python API to the cart DB. `CartDb` provides `create()`, `find()`, `update()`, `purchase()`, and `unpurchase()` methods to manage carts across client sessions. Internally, `CartDb` uses a pandas dataframe backed by the file `cart/cart_db.pickle` to hold a table of shopping carts indexed by unique cart ID, but again one could replace the dataframe with accesses to an underlying database server. `CartDb` also provides an internal `_flush()` method to save the table of shopping carts to stable storage.

- `cart.controller.Controller`: A Python class that receives cart creation, update, and checkout requests, and then calls `CatalogDb` and `CartDb` methods as appropriate to complete the requests. One could wrap `Controller` as a Python Flask app to convert it into web service with a REST API.

## Demonstration

`python-cart` includes a simple `demo.py` that creates and retrieves shopping carts from the demonstration implementation. To run the demonstration:

```
pip install pandas
./demo.py
```

`demo.py` shows off the following functionality:

1. Retrieving previously created and updated, but otherwise unpurchased carts.

1. Checking out previously unpurchased carts.

1. Creating and updating new carts.

1. Saving unpurchased carts at the end of a session.

`demo.py` is randomized to create but not necessarily check out carts over sessions. Thus, the sets of purchased and unpurchased carts will evolve over time unless one deletes the `cart/cart_db.pickle` backing file, giving one the opportunity to see how the demonstration implementation saves carts across sessions.
