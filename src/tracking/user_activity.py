# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="francescopischedda"
__date__ ="$28-feb-2012 12.12.17$"

from persistence import redis_connection

import datetime


def track_action(action, username, date_format):
    """track a user action"""

    date = datetime.datetime.now().strftime(date_format)

    c = redis_connection.get_connection()

    user_id = get_user_id(username)
    
    c.setbit('traking:%s:%s' % (action, date), user_id, 1)

def get_user_id(username):
    """
    returns the id associated with the username
    if it is not already tracked it will be added to the users collection
    """

    c = redis_connection.get_connection()

    id = c.get('users:%s:id' % username)

    if id is None:

        print 'untracked user %s' % username
        id = c.incr('users.last.id')

        if c.setnx('users:%s:id' % username, id) == 0:

            id = c.get('users:%s:id' % username)

    print '%s has id %s' % (username, id)
    return id

def report_today_users_activity(action):
    """return how many users have done 'action' today"""

    date = datetime.datetime.now().strftime("%Y-%m-%d")

    c = redis_connection.get_connection()

    count = c.get('traking:%s:%s' % (action, date))

    return count
if __name__ == "__main__":

    track_action('login','fra',"%Y-%m-%d")
    track_action('login','fra1',"%Y-%m-%d")

    print report_today_users_activity('login')
