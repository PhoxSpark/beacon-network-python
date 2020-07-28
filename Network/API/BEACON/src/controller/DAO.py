"""Database Acces Object
This will need the PosgreSQL database running on a valid URL.
You can edit the settings for the database on the database.ini
configuration file.
"""
import logging as log
import psycopg2

class AccesDataBase():
    """Object to access the database.
    The information will be taken from the configuration file found on
    the main package.
    """

    def __init__(self):
        """Initialize the object
        """
        self.connection = None
        self.cursor = None
        self.response = list()

    def simple_select_data(self, table):
        """Make a select query on the database
        Specifying the table it will take all the rows from the specified
        table.

        :param table: [description]
        :type table: [type]
        """
        self.response = list()
        #Handle exception in case the database can't be reached or the
        #syntax where incorrect.
        try:
            #Simple select
            postgre_select_query = "select * from " + table

            #Executing the query and saving it on table_record
            log.info("Selecting rows from %s table.", table)
            self.cursor.execute(postgre_select_query)
            table_record = self.cursor.fetchall()

            #Getting column names.
            column_names = [desc[0] for desc in self.cursor.description]

            #Build the dictionary from the description and the rows.
            for row in table_record:
                db_dictionary = dict()
                for i, cel in enumerate(row):
                    db_dictionary[column_names[i]] = cel
                self.response.append(db_dictionary)

        except (Exception, psycopg2.Error) as error:                                                # pylint: disable=broad-except
            log.error("Error while fetching data from PostgreSQL: %s", error)

    def complex_select_data(self, query):
        """Select with a custom SQL line

        :param query: custom sql line
        :type query: str()
        """
        self.response = list()
        try:
            self.cursor.execute(query)
            table_record = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            #Build the dictionary from the description and the rows.
            for row in table_record:
                db_dictionary = dict()
                for i, cel in enumerate(row):
                    db_dictionary[column_names[i]] = cel
                self.response.append(db_dictionary)

        except (Exception, psycopg2.Error) as error:                                                # pylint: disable=broad-except
            log.error("Error while fetching data from PostgreSQL: %s", error)

    def connect(self, database_access):
        """Make connection to the database
        Take the database on database.ini and make a connection.

        :param database_access: database to connect
        :type database_access: str()
        """
        try:
            #Make connection with the data from the database.ini
            self.connection = psycopg2.connect(
                user=database_access["user"],
                password=database_access["password"],
                host=database_access["url"],
                port=database_access["port"],
                database=database_access["database"]
            )
            self.cursor = self.connection.cursor()
        except (Exception, psycopg2.Error) as error:                                                # pylint: disable=broad-except
            log.error("Error while connecting to database: %s", error)

    def disconnect(self):
        """Disconnect from database.
        """
        #closing database connection.
        if self.connection:
            self.cursor.close()
            self.connection.close()
            log.debug("PostgreSQL connection is closed.")
