from item import Item


def test_unserialization_serialization():

    item = Item('item', 1, True)

    s = item.serialize()

    unserialized = Item.unserialize(s)

    assert unserialized == item
