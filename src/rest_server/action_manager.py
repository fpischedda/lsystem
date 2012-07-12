#! /usr/bin/python

# Action handling and dispatching functions

__author__="francescopischedda"
__date__ ="$30-dic-2011 16.57.16$"

import actions.water
import actions.helpers

from rest_server import settings

def handle_action(action, parameters):
    """
    Action dispatcher
    parameters:
    action: the name of the action to perform
    parameters: a dict with all the provided parameters
    """

    try:
        action_name = settings.Settings.get_instance().actions[action]["function"]
        func = get_func(action_name)
    except KeyError:
        return {'result' : 'KO', 'error':'action %s not found' % action}

    return func(parameters)

def get_func(path):
    """
    returns the function resolving the import path
    starting from the action module
    """
    mods = path.split(".")

    func = getattr(actions,mods[0])
    for m in mods[1:]:
    	func = getattr(func,m)

    return func


if __name__ == "__main__":
    pass