# python-cart

Cart server: main web server interface for the client user agent.

IDP: identify provider for authenticating clients.

Catalog DB: database server that hosts the inventory database.

Cart DB: database server for saving carts in flight - allows re-accessing of carts to authenticated users from any user agent

Checkout server: receive filled-out cart, process payment, zero-out cart contents
