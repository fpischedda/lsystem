from nose.tools import raises
from item import Item
from item import ItemNotUsableException


def tes_usable_item():

    i = Item('name', 10, True)
    quantity = 10

    assert quantity == i.use(quantity)


def test_usable_item_small_quantity():

    i = Item('name', 5, True)
    quantity = 10

    assert quantity > i.use(quantity)


@raises(ItemNotUsableException)
def test_not_usable_item():

    i = Item('name', 10, False)
    quantity = 10

    i.use(quantity)
