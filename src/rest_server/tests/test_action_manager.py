from rest_server import action_manager
import rest_server


def function_to_call(value):
    return value


def test_get_func():

    f_name = "tests.test_action_manager.function_to_call"
    f = action_manager.get_func(f_name, rest_server)

    assert f(1) == 1


def test_run_action():

    f_name = "tests.test_action_manager.function_to_call"

    action_manager.load_actions({'test_action': f_name}, rest_server)

    assert action_manager.run_action('test_action', {'value': 1}) == 1
