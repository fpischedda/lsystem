#! /usr/bin/python

# EnvironmentsAutomator takes care of users environments updating the plants
# contained in each environment

__author__="francescopischedda"
__date__ ="$4-feb-2012 21.47.40$"

import datetime
import user_manager

def static_get_instance():

    instance = EnvironmentsAutomator()
    while True:
       yield instance

get_instance = static_get_instance().next

class EnvironmentsAutomator(object):
    """
    EnvironmentsAutomator takes care of users environments updating the plants
    contained in each environment
    after each update the user object is saved on the correct storage engine
    """
    def __init__(self):

        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at

    def update(self):

        now = datetime.datetime.now()

        diff_time = now - self.updated_at

        users = user_manager.get_instance().get_users()

        for u in users:

            self.update_user_environments(u, now)
            
        self.updated_at = now

        return diff_time

    def update_user_environments(self, user, now):

        um = user_manager.get_instance()

        for e in user.environments.values():

            e.update(now)

            um.save_user(user)
            
            
if __name__ == "__main__":
    print "Hello World";
