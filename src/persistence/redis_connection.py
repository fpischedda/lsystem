#! /usr/bin/python

# Redis connection
# testing some of the persistence on redis

import desir
import datetime

__author__="francescopischedda"
__date__ ="$26-feb-2012 13.23.01$"

def __static_get_instance():

    instance = RedisConnectionsManager()
    while True:
       yield instance

get_instance = __static_get_instance().next

def get_connection():

    return get_instance().get_connection()

class RedisConnectionsManager(object):

    def __init__(self):

        self.connection = desir.Redis()
        #self.connection.drop_database('lsystem-development')

    def get_connection(self):

        return self.connection

if __name__ == "__main__":
    print "Hello World";


    c = get_connection()

    print c.keys("*")

    id = c.incr("timeline.last.id")

    c.set("timeline:%s:text" % id, 'fra')
    c.set("timeline:%s:username" % id, 'paraba')
    c.set("timeline:%s:datetime" % id, datetime.datetime.now().isoformat())

    print c.get("timeline:%s:text"%id)