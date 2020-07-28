# Beacon service
This service will access a stablished database (database.ini). Its queries are
meant to give a boolean answer in case a desired information exists on the
databa base or not, but it can give more information with some parameters.

Endpoint list:
--------------
- /info: It has no parametters and will give information about the service like the
type, name, id or URL.
- /query: It will take all the specified parameters (can be found on the /spec endpoint) and query the database.
- /spec: Swagger specification.