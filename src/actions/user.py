import session_manager
import user_manager

from messaging import timeline

#! /usr/bin/python

# User related functions

__author__="francescopischedda"
__date__ ="$30-gen-2012 15.16.20$"

def register(parameters):
    """
    try to register a user, provided its username and password
    if successful return the OK result and the session_id
    otherwhise KO will be returned
    """

    user = user_manager.get_instance().register_user(parameters['username'],
                                                    parameters['password'],
                                                    parameters['email'])

    if user:
        s = session_manager.get_instance().new_session(user)
        timeline.write_to_timeline('admin', "Welcome to the new user %s!" % parameters['username'])
        return {'result':'OK', 'session_id':s.id}
    else:
        return {
            'result':'KO',
            'reason':'username %s already registered' % parameters['username']
            }

def login(parameters):
    """
    try to login a user, provided its username and password
    if successful return the OK result and the session_id
    otherwhise KO will be returned
    """

    user = user_manager.get_instance().login(parameters['email'], parameters['password'])

    if user:
        s = session_manager.get_instance().new_session(user)
        timeline.write_to_timeline('admin', "L'utente %s si e' collegato..." % user.username)
        return {'result':'OK', 'session_id':s.id, 'username':user.username}
    else:
        return {'result':'KO', 'reason':'wrong login'}

def logout(parameters):
    """
    close the specified session
    """

    u = parameters['session'].user

    user_manager.get_instance().logout(u.username)
    
    session_manager.get_instance().close_session(parameters['session'].id)

    timeline.write_to_timeline('admin', "L'utente %s si e' scollegato, ciao..." % user.username)
    return {'result':'OK'}

def items(parameters):

    u = parameters['session'].user

    items = [ i.serialize() for i in u.items.values()]
    
    return {'result': 'OK', 'items' : items}

def environments(parameters):
    """
    returns the list of alla available environments of the user who has made
    the request
    """

    try:
        username = parameters['username']
        u = user_manager.get_instance().get_user(username)
    except KeyError:
        u = parameters['session'].user

    if u != None:
        env = [e.serialize() for e in u.environments.values()]
        timeline.write_to_timeline('admin', "L'utente %s sta controllando le sue serre..." % u.username)
        return {'result':'OK', 'environments':env}

    return {'result':'KO', 'reason':'user %s not found' % parameters['username']}

def plant(parameters):

    try:
        username = parameters['username']
        u = user_manager.get_instance().get_user(username)
    except KeyError:
        u = parameters['session'].user

    if u != None:

        try:
            p = u.plants[parameters['name']]
            timeline.write_to_timeline('admin', "User %s is looking at the plant %s..." % (u.username,parameters['name']))
            return {'result':'OK', 'plant':p.serialize()}

        except KeyError:
            return {'result':'KO', 'reason':'user\'s plant %s not found' % parameters['name']}

    return {'result':'KO', 'reason':'user %s not found' % parameters['username']}

def get_all_names(parameters):

    users = user_manager.get_instance().get_all_names()
    
    return {'result':'OK', 'users':users}

def environment_details(parameters):

    try:
        username = parameters['username']
        u = user_manager.get_instance().get_user(username)
    except KeyError:
        u = parameters['session'].user

    if u != None:
        try:
            e = u.environments[parameters['name']]
        except:
            return {
                'result':'KO',
                'reason':'unavailable environment %s for the selected user' % parameters['name']
                }

        return {'result':'OK', 'environmant':e.serialize()}


    return {'result':'KO', 'reason':'user %s not found' % parameters['username']}

if __name__ == "__main__":
    print "Hello World";
