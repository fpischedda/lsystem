from rest_server import actions_definition
from rest_server import action_manager
from rest_server import url_parser


class AuthException(Exception):
    pass


def init(actions_dict, actions_module):

    actions_definition.load(actions_dict)
    func_dict = {k: v['function'] for k, v in actions_dict.iteritems()}
    action_manager.load_actions(func_dict, actions_module)


def call(url, get_session_func):
    action_name, parameter_list = url_parser.parse(url)

    action = actions_definition.select(action_name)

    if action['protected']:
        session = get_session_func(parameter_list[0])

        if session is None:
            raise AuthException

        parameters = url_parser.parse_parameters(action['parameters'],
                                                 parameter_list[1:])

        parameters['session'] = session
    else:
        parameters = url_parser.parse_parameters(action['parameters'],
                                                 parameter_list)

    return action_manager.run_action(action_name, parameters)
