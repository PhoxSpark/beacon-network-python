# Beacon Network

This is the implementation by the INB Life Sciences of the Beacon Network in Python. You have a description of all the services on it's respective modules, but the only one planed to be developed is the PyBA one (Python Beacon Aggregator).

Deployment
----------
This service is ready for deployment using docker-compose. Simply you can use:
```bash
docker-compose up --build
```
Then the service will start to build and deploy. It shouls work out of the box without any configuration, the docker-compose.yml and the dockerfiles have some hardcode  information to allow the services to work out of the box.

One thing that may you will be interested to do once the services are running is to execute the url http://localhost:5004/registered_beacons with PUT method to get the aggregator to update its network configuration file asking the registry.

To drop the services, simply press Ctrl+C or `docker-compose down` if you run it with the -d flag.

Individual service execution
----------------------------
Each service can run individually, just go to the path `./Network/api` and execute `python -m `_name of the service_, you can use the flag `-h` to see all the available flags. In the case of the database, you can use the Makefile found in the path `./Network`.

Note
----
I recommend to use the /spec endpoint present on every service (except the database) to test the services, but I've used Postman while developing and debuging.
