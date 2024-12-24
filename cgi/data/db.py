import mysql.connector
import data.db_config


class Db:
    def __init__(self):
       self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = mysql.connector.connect(**data.db_config.mysql_connection_data)
        return self.connection