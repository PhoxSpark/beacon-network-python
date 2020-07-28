# Flask Blueprints

There are all the blueprints for Flask to use. Each one of these blueprints represents a Flask endpoint for the PyBA API. The ones that are the same endpoints but have attributes are in the same file. To add new blueprints you have to add it on this folder, register on the **__init__.py** file of this folder and add a line on the **api.py** file.

## Modularization

With this system of blueprints, it can be pretty easy to modularize the endpoints. This will mean that everyone can programm a new endpoint, add it into this folder and run it on PyBA, like a plug-in. This modularization is not programmed/available for security and compatibility reasons, but in case someone need it or thinks it's a good idea, I can make it work o make a standalone patch for who want it.