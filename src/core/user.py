# module that define a User object
# a user has list of plants, a credit balance
# and a list of items to use
__author__ = "francescopischedda"
__date__ = "$27-mag-2011 17.04.07$"


from plant import Plant
from environment import Environment
from item import Item


def new_user(username, password, email):
    """
    create a new user with a natural environment and a default plant
    """

    u = User(username, password, email)

    u.add_environment(Environment('natural'))

    u.add_plant_to_environment(Plant.randomize_default(), 'natural')
    u.add_item(Item('water-tank', 10, False))
    u.add_item(Item('water-reserve', 10, True))
    u.add_item(Item('magic-bottle', 100, True))

    return u


class User(object):

    @classmethod
    def unserialize(cls, obj):

        inst = cls(obj['username'], obj['password'], obj['email'])

        for i in obj['items']:

            inst.items[i['name']] = Item.unserialize(i)

        for e in obj['environments']:

            env = Environment.unserialize(e)
            inst.environments[env.name] = env

            for p in env.plants.values():

                inst.plants[p.name] = p

        return inst

    def __init__(self, username, password, email):

        self.username = username
        self.password = password
        self.email = email

        self.environments = {}
        self.plants = {}
        #items are store as name=>count
        #when an item count is <= 0 the entry is removed
        self.items = {}

    def add_item(self, item):
        """
        add an item to the inventory
        """

        try:
            self.items[item.name].quantity + item.quantity
        except KeyError:
            self.items[item.name] = item

    def use_magic_bottle(self, plant_name):
        """
        returns 0 on success, 1 if the item is not found,
        """

        if self.use_item('magic-bottle', 1) == 0:
            return 1

        try:
            self.plants[plant_name].fill_water()
        except KeyError:
            return 2

        #do one hour of light_on_cycle and one hour of light_off_cycle
        times = 60
        p = self.plants[plant_name]
        while times > 0:
            p.light_on_cycle(60)
            p.light_off_cycle(60)
            p.fill_water()
            times -= 1

        return 0

    def use_item(self, item_name, quantity):
        """
        try to use an item
        returns the effectively used quantity
        """
        try:

            if self.items[item_name].usable is False:
                return 0

            self.items[item_name].quantity -= quantity

            if self.items[item_name].quantity < 0:
                quantity += self.items[item_name].quantity
                del self.items[item_name]
        except KeyError:
            return 0

        return quantity

    def remove_item(self, item_name):
        """
        remove an item from the inventory
        """

        count = 0
        try:
            count = self.items[item_name]
        finally:

            count -= 1

            if count > 0:

                self.items[item_name] = count
            else:

                del self.items[item_name]

    def add_environment(self, environment):

        self.environments[environment.name] = environment

    def add_plant_to_environment(self, plant, environment_name):

        try:
            self.environments[environment_name].add_plant(plant)
            self.plants[plant.name] = plant
        except KeyError:
            print "unavailable environment"

    def add_plant(self, plant):

        self.plants[plant.name] = plant

    def serialize(self):

        envs = [e.serialize() for e in self.environments.values()]
        plants = [p.serialize() for p in self.plants.values()]
        items = [i.serialize() for i in self.items.values()]

        ret = {'username': self.username,
               'password': self.password,
               'email': self.email,
               'plants': plants,
               'environments': envs,
               'items': items}

        return ret
