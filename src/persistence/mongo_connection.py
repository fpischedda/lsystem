# To change this template, choose Tools | Templates
# and open the template in the editor.
import pymongo


def static_get_instance():

    instance = MongoConnectionsManager()
    while True:
        yield instance

get_instance = static_get_instance().next


def get_default_db():

    return get_instance().get_default_db()


class MongoConnectionsManager(object):

    CONNECTION_STRING = 'localhost'
    DEFAULT_DB = 'checkers'

    def __init__(self):

        self.connection = pymongo.Connection(self.CONNECTION_STRING)
        #self.connection.drop_database('lsystem-development')

    def get_connection(self):

        return self.connection

    def get_default_db(self):

        db = self.connection[self.DEFAULT_DB]
        return db

    def get_db(self, db_name):

        return self.connection[db_name]
