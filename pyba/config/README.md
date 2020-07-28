
# Config files information

This information are the "removed by the service" anotations of the config files.

## params.conf

This file contains the parameters of the service. This can be modified by the user at their own risk, but probably this will accept everything the user inputs because the read of the file is maded automatically by the library "configparser" and it's very flexible.

Note: A lot of parameters will be just text or information to show on the API endpoint specified and the program will never look if the data is correct because it does not have sense, the user is responsible of the accurancy of the text data like the ID or Name. The parameters with some  limits like the "open" one (true or false) will be tested by the program. Also, this file can and will be edited by the program to add some information or modify things.

Note: APP version and API version are defined by the service, not by the user. If you change it, it will change back. To edit this, you need to edit the __init__.py found on the same place as __main__.py, but it's not recommended.