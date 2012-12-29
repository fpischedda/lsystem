from rest_server import url_parser


def test_parse():

    action, parameters = url_parser.parse('example.com/test_func/value')

    assert action == 'test_func'
    assert parameters == ['value']


def test_parse_parameters():

    parameters = [{'name': 'a_parameter', 'optional': False}]
    values = ['a value']

    resolved = url_parser.parse_parameters(parameters, values)

    assert resolved['a_parameter'] == values[0]
