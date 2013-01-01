from rest_server import url_action_caller


def protected_func(session):
    return True


def invalid_session(sid):
    return None


def valid_session(sid):
    return ('a user', 'some user value')


def test_call_by_url_protected_valid_sid():

    actions = {'test_act': {'function': 'protected_func',
                            'parameters': [],
                            'protected': True}}

    url_action_caller.init(actions, __name__)

    res = url_action_caller.call('example.com/test_act/1234', valid_session)

    assert res is True
