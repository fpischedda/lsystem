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

    p = action_parameters
    pos = 0
    for k in p:

        try:
            params[k['name']] = parameter_list[pos]
            pos += 1
        except IndexError as ex:
            if k['optional'] is False:
                raise ex
            else:
                break

    return params
