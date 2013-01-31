from rest_server.session import Session


def test_session_creation():

    s = Session(1, '127.0.0.1', 'test')

    s.save()

    ss = Session.get_by_user_id(1)

    assert s.user_id == ss.user_id
