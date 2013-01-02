from nose.tools import raises
from rest_server import url_action_caller


def unprotected_func(some_param):
    return some_param


def protected_func(session):
    return True


def invalid_session(sid):
    return None


def valid_session(sid):
    return ('a user', 'some user value')


@raises(url_action_caller.AuthException)
def test_call_by_url_protected_invalid_sid():

    actions = {'test_act': {'function': 'protected_func',
                            'parameters': [],
                            'protected': True}}

    url_action_caller.init(actions, __name__)

    res = url_action_caller.call('example.com/test_act/1234', invalid_session)

    assert res is True


def test_call_by_url_protected_valid_sid():

    actions = {'test_act': {'function': 'protected_func',
                            'parameters': [],
                            'protected': True}}

    url_action_caller.init(actions, __name__)

    res = url_action_caller.call('example.com/test_act/1234', valid_session)

    assert res is True


def test_call_by_url_unprotected():

    actions = {'act': {'function': 'unprotected_func',
                       'parameters': [{'name': 'some_param',
                                       'optional': False}],
                       'protected': False
                       }}

    url_action_caller.init(actions, __name__)

    res = url_action_caller.call('example.com/act/some_value', valid_session)

    assert res == 'some_value'
