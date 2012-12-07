# item utility class
__author__ = "francescopischedda"
__date__ = "$13-mar-2012 16.19.40$"
from utils.equality_comparable import EqualityComparable


class ItemNotUsableException(Exception):
    pass


class Item(EqualityComparable):

    def __init__(self, name, quantity, usable, user_id):

        self.name = name
        self.usable = usable
        self.quantity = quantity
        self.user_id = user_id

    def use(self, quantity):

        if not self.usable:
            raise ItemNotUsableException

        if quantity > self.quantity:
            quantity = self.quantity

        self.quantity -= quantity

        return quantity
