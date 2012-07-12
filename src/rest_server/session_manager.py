#! /usr/bin/python

# class to manage user sessions

__author__="francescopischedda"
__date__ ="$30-gen-2012 12.00.07$"

import time
import uuid

def static_get_instance():

    instance = SessionManager()
    while True:
       yield instance

get_instance = static_get_instance().next

class SessionManager(object):

    MAX_INACTIVE_SECONDS = 60*60

    def __init__(self):

        #there can be only a session per user
        self.sessions = {}
        self.sessions_by_id = {}

    def new_session(self, user, ip='127.0.0.1', device='web'):
        """
        create a new session for the specified user
        """

        s = Session(user, ip, device)
        self.sessions[user.username] = s
        self.sessions_by_id[s.id] = s
            
        return s

    def close_session(self, session_id):
        """
        close a session identified by it id
        """
        s = self.sessions_by_id[session_id]

        del self.sessions_by_id[session_id]
        del self.sessions[s.user.username]

    #return the active session of the username
    #if the user has not an active session None is returned
    def user_session(self, username):

        try:

            return self.session[username]
        except KeyError:
            return None

    #return all active user's sessions
    def active_sessions(self):

        return self.sessions.values()

    #delete session of inactive users
    #return the number of deleted sessions
    def delete_inactive_users(self):

        now = time.time

        count = 0
        for s in self.sessions.values():

            if now - s.last_operation_date > SessionManager.MAX_INACTIVE_SECONDS:

                count += 1
                del self.sessions[s.user.username]
                del self.sessions_by_id[s.id]

        return count

    #return the session object identified by the session id
    #if the session is not found None is returned
    def get_session(self, session_id):

        try:
            return self.sessions_by_id[session_id]
        except KeyError:
            return None
        
#class that define a session for a user
class Session(object):

    def __init__(self, user, ip, device):

        self.id = uuid.uuid4().hex
        self.user = user
        self.ip = ip
        self.device = device
        self.start_date = time.time
        self.close_date = None
        self.last_operation_date = time.time

if __name__ == "__main__":

    import user_manager
    
    s = Session('foca', '127.0.0.1','default')

    print(s)

    um = user_manager.get_instance()
    sm = SessionManager(um)

    s = sm.new_session('foca','password', '127.0.0.1', 'default')

    print 'logged in user %s' % (s.user.username,)

    print('active users:')

    for s in sm.active_sessions():
        
        print(s.user.username)
