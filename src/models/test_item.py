from models.item import ItemModel


def test_model_creation():

    item = ItemModel('item_name', 10, True, '12345')

    assert item.name == 'item_name'
    assert item.quantity == 10
    assert item.usable is True
    assert item.user_id == '12345'


def test_serialization():

    item = ItemModel('item_name', 10, True, '12345')

    expected_serialization = {'name': 'item_name',
                              'quantity': 10,
                              'usable': True,
                              'user_id': '12345'}

    assert item.serialize() == expected_serialization


def test_unserialization():

    item = ItemModel('item_name', 10, True, '12345')

    serialized = item.serialize()

    assert item == ItemModel.unserialize(serialized)
