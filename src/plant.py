from trunk import Trunk

# this module handles the logic about the plant and its needs

__author__="francescopischedda"
__date__ ="$22-mag-2011 17.19.16$"

def create_tree(tree, level, max_trunk_length):

    if level > 0 :

        new_trunks = Trunk.next_children(tree.type, max_trunk_length)

        if level > 1:
            for t in new_trunks:
                create_tree(t, level - 1, max_trunk_length)

        tree.children = new_trunks

class Plant(object):

    @classmethod
    def unserialize(cls, obj):

        p = cls(obj['name'], obj['genre'], obj['max_trunk_length'],
            obj["pot_water_capacity"], obj["available_water"])

        p.base_trunk = Trunk.unserialize(obj['plant'])

        return p

    @classmethod
    def randomize_default(cls, name='default'):

        return cls.randomize(name, 3, 30, 10, 10)
    
    @classmethod
    def randomize(cls, name, start_level, max_trunk_length, pot_capacity, initial_water):

        p = cls(name, 'random', max_trunk_length, pot_capacity, initial_water)

        p.max_trunk_length = max_trunk_length

        p.base_trunk = Trunk.randomize_default('a', max_trunk_length)

        create_tree(p.base_trunk, start_level, max_trunk_length)

        return p

    def __init__(self, name='', genre='random',max_trunk_length=30, pot_capacity=10, initial_water=10):

        self.max_trunk_length = max_trunk_length

        self.base_trunk = None

        #water misures are expressed as liters
        self.pot_water_capacity = pot_capacity
        self.available_water = initial_water

        self.genre = genre
        self.name = name

        self.lights_on_grow_scale = 0.1
        self.lights_off_grow_scale = 1.0

        self.lights_on_eat_scale = 1.0
        self.lights_off_eat_scale = 0.1

    def grow(self, seconds):

        self.base_trunk.grow(seconds)

    def light_on_cycle(self, seconds):

        sec = seconds*self.lights_on_grow_scale
        self.base_trunk.grow(sec)
        self.base_trunk.keep_alive(sec)
        
        sec = seconds*self.lights_on_eat_scale
        return self.eat(sec)

    def light_off_cycle(self, seconds):

        sec = seconds*self.lights_off_grow_scale
        self.base_trunk.grow(sec)
        self.base_trunk.keep_alive(sec)

        sec = seconds*self.lights_off_eat_scale
        return self.eat(sec)

    def water_needed(self):
        """
        returns the water needed by this plant
        """
        return self.base_trunk.water_needed()

    def eat(self, seconds):

        food_used = self.base_trunk.eat(seconds, self.available_water)
        self.available_water -= food_used

        return food_used

    def keep_alive(self):

        self.base_trunk.keep_alive()

    def fill_water(self):

        self.available_water = self.pot_water_capacity

    def add_water(self, water_amount):

        self.available_water += water_amount

        if self.available_water > self.pot_water_capacity:
            self.available_water = self.pot_water_capacity

        return self.available_water

    def serialize(self):

        return {'name':self.name, 'genre':self.genre,
            'max_trunk_length':self.max_trunk_length,
            'available_water':self.available_water,
            'pot_water_capacity':self.pot_water_capacity,
            'plant':self.base_trunk.serialize()}
        
if __name__ == "__main__":

    p = Plant.randomize('test', 2, 30, 6.0, 4.0)

    ps = p.serialize()
    print ps

    pus = Plant.unserialize(ps)
    print pus

    test_time = 60.0 * 60 * 12

    print( "lights off cycle %s seconds" % test_time )
    used_water = p.light_off_cycle(test_time)

    print( "ramaining water after %s seconds of light_off_cycle: %s" % (test_time, p.available_water))

    print( "lights on cycle %s seconds" % test_time )
    used_water = p.light_on_cycle(test_time)

    print( "ramaining water after %s seconds of light_on_cycle: %s" % (test_time, p.available_water))

    print( "lights off cycle %s seconds" % test_time )
    used_water = p.light_off_cycle(test_time)

    print( "ramaining water after %s seconds of light_off_cycle: %s" % (test_time, p.available_water))

    print( "lights on cycle %s seconds" % test_time )
    used_water = p.light_on_cycle(test_time)

    print( "ramaining water after %s seconds of light_on_cycle: %s" % (test_time, p.available_water))
