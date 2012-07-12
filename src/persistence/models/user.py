# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="francescopischedda"
__date__ ="$25-apr-2012 16.12.02$"

from persistence import mongo_connection
import user

class User:

    @staticmethod
    def store(user):

        db = mongo_connection.get_instance().get_default_db()
        u = user.serialize()

        db.users.insert(u)

    @staticmethod
    def update(user):

        db = mongo_connection.get_default_db()
        db.users.update({'email':user.email}, user.serialize())

    @staticmethod
    def retrive_by_username(email):

        user_obj = None
        db = mongo_connection.get_default_db()
        u = db.users.find_one( {'username':username})

        if u is not None:
            user_obj = user.User.unserialize(u)

        return user_obj

    @staticmethod
    def retrive_by_email(email):

        user_obj = None
        db = mongo_connection.get_default_db()
        u = db.users.find_one( {'email':email})

        if u is not None:
            user_obj = user.User.unserialize(u)

        return user_obj

    @staticmethod
    def get_all_usernames():

        db = mongo_connection.get_default_db()
        users = db.users.find({}, {'username':1})

        return [u['username'] for u in users ]


if __name__ == "__main__":
    print "Hello World"
