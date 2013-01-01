# class to manage user sessions
__author__ = "francescopischedda"
__date__ = "$30-gen-2012 12.00.07$"
from rest_server.session import Session


__MAX_INACTIVE_SECONDS = 60 * 60


def new_session(self, user_id, ip='127.0.0.1', device='web'):
    """
    create a new session for the specified user
    """

    s = Session.get_by_user_id(user_id)

    if s is None or s.expired(__MAX_INACTIVE_SECONDS):
        s.delete()
        s = Session(user_id, ip, device)
        s.insert()

    return s


def close_session(self, id):
    """
    close a session identified by it id
    """
    Session.close_by_id(id)


def user_session(self, user_id):
    """
    return the active session of the username
    if the user has not an active session None is returned
    """
    return Session.get_by_user_id(user_id)


def get_session(self, id):

    return Session.get_by_id(id)
