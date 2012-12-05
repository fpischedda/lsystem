# item utility class
__author__ = "francescopischedda"
__date__ = "$13-mar-2012 16.19.40$"
from utils.equality_comparable import EqualityComparable


class Item(EqualityComparable):

    def __init__(self, name, quantity, usable, user_id):

        self.name = name
        self.usable = usable
        self.quantity = quantity
        self.user_id = user_id
