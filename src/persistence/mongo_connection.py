#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="francescopischedda"
__date__ ="$12-feb-2012 16.07.54$"

import pymongo

def static_get_instance():

    instance = MongoConnectionsManager()
    while True:
       yield instance

get_instance = static_get_instance().next

def get_default_db():

    return get_instance().get_default_db()

class MongoConnectionsManager(object):

    def __init__(self):

        self.connection = pymongo.Connection('mongodb://minasss:f0c4land@dbh26.mongolab.com:27267/lsystem-development')
        #self.connection.drop_database('lsystem-development')

    def get_connection(self):

        return self.connection

    def get_default_db(self):

        db = self.connection['lsystem-development']
        #db.authenticate('minasss', 'f0c4land')
        return db
    
if __name__ == "__main__":

    m = get_instance()
    print m

    c = m.get_connection()
    print c

    db = c.lsystem_development
    print db



