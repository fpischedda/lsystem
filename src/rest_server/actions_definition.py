# maintains action definitions loaded passing a dict whose keys are the
# action names and values are action properties
# an action has an associated function, an optional list of parameters
# and can be protected (user need to be logged in some how)

__actions = {}


def load(actions,
         default_definition={'function': '',
                             'parameters': [],
                             'protected': True}):

    a = {}
    for k, v in actions.iteritems():
        new_action = v

        #load the default definition of a function
        action = default_definition.copy()

        #merge defaults with user specified function properties
        action.update(new_action)

        a[k] = action

    global __actions
    __actions = a

    return a


def select(action_name):
    #get the action definition

    try:
        action = __actions[action_name]

    except KeyError:
        return None

    return action
