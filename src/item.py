# item utility class

__author__="francescopischedda"
__date__ ="$13-mar-2012 16.19.40$"

class Item(object):

    @classmethod
    def unserialize(cls, obj):

        inst = cls(obj['name'], obj['quantity'], obj['usable'])
        return inst

    def serialize(self):

        return {
            'name':self.name, 'usable':self.usable,
            'quantity':self.quantity}

    def __init__(self, name, quantity, usable):

        self.name = name
        self.usable = usable
        self.quantity = quantity

if __name__ == "__main__":

    i = Item('itemname', 1.0, False)

    ser = i.serialize()

    print ser


    print i.unserialize(ser)

    unser = Item.unserialize(ser)

    print unser
