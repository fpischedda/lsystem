# url and parameters parser
# Francesco Pischedda 29-12-2012


def parse(query_string):
    """
    Action parser
    parameters:
    query_string: the requested query string to be parsed
    returns:
    the action name and the corresponding parameters dict
    """

    splitted = query_string.split("/")
    action_name = splitted[1]

    return action_name, splitted[2:]


def parse_parameters(action_parameters, parameter_list):
    """
    Parse the parameter list using the action name
    parameters:
    action: the name of the action
    parameter_list: list of parameters to be translated to a dict
    """

    params = dict()

    pos = 0
    for p in action_parameters:

        try:
            params[p['name']] = parameter_list[pos]
        except IndexError as ex:
            if p['optional'] is False:
                raise ex
            else:
                params[p['name']] = None

        pos += 1

    return params
