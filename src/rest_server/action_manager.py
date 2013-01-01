# Action handling and dispatching functions
__author__ = "francescopischedda"
__date__ = "$30-dic-2011 16.57.16$"
import importlib


__action_to_function = None


def load_actions(actions, root_module_name):
    """
    load the speficied functions associated to an action name
    parameters:
        - actions a dict (or a ky-value container) where key is the action name
        and the value is the function name
    """

    root_module = importlib.import_module(root_module_name)

    global __action_to_function
    __action_to_function = {k: get_func(v, root_module)
                            for k, v in actions.iteritems()}


def run_action(action, parameters):
    """
    Action dispatcher
    parameters:
    action: the name of the action to perform
    parameters: a dict with all the provided parameters
    """

    try:
        func = __action_to_function[action]
    except KeyError:
        return {'result': 'KO', 'error': 'action %s not found' % action}

    return func(**parameters)


def get_func(path, root_module):
    """
    returns the function resolving the import path
    starting from the specified (root_module) module
    """

    mods = path.split(".")
    func = getattr(root_module, mods[0])
    for m in mods[1:]:
        func = getattr(func, m)

    return func
