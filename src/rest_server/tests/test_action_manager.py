from rest_server import action_manager
import importlib


def function_to_call(value):
    return value


def test_get_func():

    f_name = "function_to_call"

    root_module = importlib.import_module('rest_server.tests.test_action_manager')
    f = action_manager.get_func(f_name, root_module)

    assert f(1) == 1


def test_run_action():

    f_name = "tests.test_action_manager.function_to_call"

    action_manager.load_actions({'test_action': f_name}, 'rest_server')

    assert action_manager.run_action('test_action', {'value': 1}) == 1
