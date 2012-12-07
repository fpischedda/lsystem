from nose.tools import raises
from item import Item
from item import ItemNotUsableException


def tes_usable_item():

    i = Item('name', 10, True, 0)
    quantity = 10

    assert quantity == i.use(quantity)


def test_usable_item_small_quantity():

    i = Item('name', 5, True, 0)
    quantity = 10

    assert quantity > i.use(quantity)


@raises(ItemNotUsableException)
def test_not_usable_item():

    i = Item('name', 10, False, 0)
    quantity = 10

    i.use(quantity)
