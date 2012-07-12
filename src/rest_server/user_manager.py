#! /usr/bin/python

# User Manager class

__author__="francescopischedda"
__date__ ="$29-gen-2012 22.53.23$"

import user as user_module
from persistence import mongo_connection

def static_get_instance():

    instance = UserManager()
    while True:
       yield instance

get_instance = static_get_instance().next

class UserManager:

    def __init__(self):
        #users are hold by a dictionary, username is the key
        #user object is the value
        self.users = dict()

    def register_user(self, username, password, email):
        """
        create a new user only if its username is not already in the system
        """
        u = self.get_user_by_email(email)

        if u is not None:
            return None
            
        u = user_module.new_user(username, password, email)

        self.add_user(u)

        return u
    
    def add_user(self, user_obj):
        """
        add a new user to the system
        """
        self.users[user_obj.username] = user_obj

        persistence.mongo_decorators.user.User.save(user)

    def get_user(self, username):
        """
        returns a user object
        """
            
        return persistence.mongo_decorators.users.User.retrive_by_username(username)

    def get_user_by_email(self, email):
        """
        returns a user object by email
        """
        
        return persistence.mongo_decorators.users.User.retrive_by_email(email)
    
    def get_users(self):
        """
        returns all the active users on this server
        """
        return self.users.values()

    def get_all_names(self):
        """
        returns a list of all usernames
        """

        return persistence.mongo_decorators.users.User.get_all_usernames()

    def save_all_users(self):
        
        for u in self.users.values():
            
            self.save_user(u)
            
    def save_user(self, user):

        persistence.mongo_decorators.user.User.update(user)
        
    def login(self, email, password):
        #fake login

        u = self.get_user_by_email(email)

        if u is not None:

            return u
            if u.password == password:
                return u

        return None

    def logout(self, username):

        try:

            persistence.mongo_decorators.user.User.update(self.users[username])
            
            del self.users[username]
        finally:
            pass
        
if __name__ == "__main__":

    db = mongo_connection.get_default_db()

    db.users.remove({})

    um = get_instance()
    
    ru = um.register_user('fra','fra', 'fra@fra')

    print ru
    
    u = um.login('fra@fra', 'fra')
    print u

    u = um.get_user_by_email('fra@fra')
    print u

    print u.password