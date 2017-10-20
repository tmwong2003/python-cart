# python-cart

This is an implementation of a simple Python web store and shopping cart back-end architecture.

## Architecture description

A simple back-end architecture comprises the following set of independent services:

1. A catalog database (catalog DB) that serves up descriptions of items available for sale. A basic database could maintain a simple table indexed by item SKU.

1. A cart database (cart DB) that manages shopping cart contents between client web sessions.

1. An identity provider (IDP) that manages client authentication.

1. A payment processor that charges the client once they have decided to check out with a particular cart full of items.

1. A controller service (controller) that processes incoming client requests and prepares the responses used to render the web interface on the client user agent.

The typical control flow (assuming no error conditions) during a session would be as follows:

1. A client contacts the controller.

1. The controller redirects the client to the IDP to complete an authentication process and obtain authentication credentials. We use these credentials to identify client as the owner of of one or more carts.

1. The controller contacts the cart DB to retrieve any outstanding unpurchased carts owned by the client.

1. The controller contacts that catalog DB to retrieve the items available for sale.

1. The controller presents the unpurchased carts and items available for sale to the client.

1. The client user agent browses the presented items, and submits zero or more cart updates during the session. The client associates each submitted update to a cart ID, or may create a new card 

5. Upon receiving a cart update, the controller combines the cart the update to the cart DB

Cart server: main web server interface for the client user agent.

IDP: identify provider for authenticating clients.

Catalog DB: database server that hosts the inventory database.

Cart DB: database server for saving carts in flight - allows re-accessing of carts to authenticated users from any user agent

Checkout server: receive filled-out cart, process payment, zero-out cart contents
