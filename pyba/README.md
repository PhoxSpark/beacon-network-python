# PyBA

Beacon Aggregator made by the INB - Life Sciences implemented with Python. This Beacon Aggregator (BA) will take it's own registry or consult the known registry services for get a list of Beacons to consult. The BA will redirect every unknown endpoint to all the Beacons, collecting every answer and showing it to the client/user.

PyBA workflow
-------------
The PyBA application will start by the __init__.py file, declaring some constants and configurations, after this it will execute the __main__.py file, wich first of all will read the arguments, initialize the logging and updating the "non user editable" camps on the config file. After this, the service is initialized executing the file api.py, wich will interpret the readed arguments and start the flask service. From this, it just load the endpoints on the blueprint folder when they're requested.