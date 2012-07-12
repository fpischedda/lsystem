#! /usr/bin/python

# handles timeline messaging
# used to store and retrieve system and user messages

__author__="francescopischedda"
__date__ ="$26-feb-2012 16.59.39$"

from persistence import redis_connection

import datetime

def get_messages(oldest_id, last_id):
    """
    return a list of messages whose ids are between oldset_id and last_id
    extremes included
    """
    c = redis_connection.get_connection()
    
    messages = []

    for id in range(oldest_id, last_id+1):
        msg = {
                'id': id,
                'username':c.get("timeline:%s:username"%id),
                'text':c.get("timeline:%s:text"%id),
                'datetime':c.get("timeline:%s:datetime"%id),
                'likes':c.smembers("timeline:%s:likes"%id)
                }
        messages.append(msg)

    return messages

def last_messages_by_last_id(oldest_id):
    """
    return all messages starting from oldest_id to "timeline.last.id" key value
    """
    c = redis_connection.get_connection()

    last_id = int(c.get("timeline.last.id"))

    if oldest_id<0:
        oldest_id=0

    if oldest_id == last_id:
        return []
    
    return get_messages(oldest_id, last_id)

def last_messages(count):
    """
    return the last "count" messages if there are some
    """
    c = redis_connection.get_connection()

    last_id = int(c.get("timeline.last.id"))

    oldest_id = last_id - count

    if oldest_id<0:
        oldest_id=0

    return get_messages(oldest_id, last_id)

def write_to_timeline(username, text):
    """
    write a message to the timeline
    a message has a default ttl of 24 hours
    """
    c = redis_connection.get_connection()

    id = c.incr("timeline.last.id")

    expires = 60*60*24 #timeline messages lasts one day
    c.multi()
    c.setex("timeline:%s:text" % id, expires, text)
    c.setex("timeline:%s:username" % id, expires, username)
    c.setex("timeline:%s:datetime" % id, expires, datetime.datetime.now().isoformat())
    #c.expire("timeline:%s:*" % id, )
    c.execute()
    
    return id

def like(username, id):
    c = redis_connection.get_connection()

    expires = c.ttl("timeline:%s:text" % id)

    #if the key is not found or has not an associated ttl -1 is returned
    if expires < 0:
        return

    c.multi()
    c.sadd("timeline:%s:likes" % id, username)
    c.expire("timeline:%s:likes" % id, expires)#message likes expires with the message
    c.execute()
    
if __name__ == "__main__":

    like('fra', 20)
    print last_messages(4)

    c = redis_connection.get_connection()

    expires = c.ttl("timeline:%s:text" % 60)

    print expires
