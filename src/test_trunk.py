from trunk import Trunk


def test_serialization_unserialization():

    trunk = Trunk.randomize('a', 30, 60, 20)

    s = trunk.serialize()

    unserialized = Trunk.unserialize(s)

    assert trunk == unserialized
