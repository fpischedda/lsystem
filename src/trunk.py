# this module describe a trunk as a parte of a tree
__author__ = "francescopischedda"
__date__ = "$26-mag-2011 10.11.16$"

import random
from utils.equality_comparable import EqualityComparable


class Trunk(EqualityComparable):

    #this class variable defines the amount of water needed (in liters)
    # to keep 1.0 cm of trunk length alive
    TRUNK_LENGTH_TO_WATER_NEEDS = 0.01

    #energy needed to grow for one second of growing cycle
    ENERGY_NEEDED_TO_GROW_ONE_SECOND = 0.01

    #energy needed to live for one second
    ENERGY_NEEDED_TO_LIVE_ONE_SECOND = 0.001

    #the max amount of food that can be used by the trunk in one second
    MAX_FOOD_INTAKE_ONE_SECOND = 0.01

    @classmethod
    def unserialize(cls, obj):

        inst = cls(obj['node_type'], obj['angle'],
                   obj['length'], obj['max_length'],
                   obj['max_grow_unit'], obj['energy'])

        children = [Trunk.unserialize(c) for c in obj['children']]

        inst.children = children
        return inst

    @classmethod
    def randomize(cls, type, min_angle, max_angle, max_trunk_length):

        angle = random.uniform(min_angle, max_angle)
        half_max = max_trunk_length * 0.5
        length = random.uniform(2.0, half_max)
        max_length = length + random.random() * half_max

        return cls(type, angle, length, max_length)

    @classmethod
    def randomize_default(cls, type, max_trunk_length):

        return cls.randomize(type, -0.6, 0.6, max_trunk_length)

    @classmethod
    def next_children(cls, type, max_trunk_length):

        if type == 'b':

            new = [cls.randomize_default('a', max_trunk_length)]
        else:

            new = [cls.randomize_default('a', max_trunk_length),
                   cls.randomize_default('b', max_trunk_length)]

        return new

    def __init__(self, type=0, angle=0, length=0, max_length=0,
                 max_grow_unit=4.0, energy=1.0, children=list()):
        """Init a trunk"""

        self.type = type
        self.children = children
        #angle
        self.angle = angle

        self.start_length = length
        self.current_length = length
        self.max_length = max_length

        #the max misure of how much length a trunk can grow on a full night;
        #a standard night lasts 18 hours
        self.max_grow_unit = max_grow_unit
        self.max_grow_unit_one_second = self.max_grow_unit / (3600.0 * 12)

        #the trunk's available energy, the range is 0.0 - 1.0
        #when a trunk grows it consumes its energy; lost energy will be acquired
        #from the water feeded to this trunk
        self.energy = energy

    def water_needed_by_trunk(self):

        return (1.0 - self.energy) * self.current_length * Trunk.TRUNK_LENGTH_TO_WATER_NEEDS

    def water_needed(self):
        """
        return the water required to keep this trunk and its children alive
        """
        water = self.water_needed_by_trunk()

        for t in self.children:

            water += t.water_needed()

        return water

    def energy_needed(self, seconds):
        """
        returns the amount of energy needed by this trunk and its children
        to live one second
        """
        energy = Trunk.ENERGY_NEEDED_TO_LIVE_ONE_SECOND * seconds

        if self.current_length < self.max_length:

            energy += Trunk.ENERGY_NEEDED_TO_GROW_ONE_SECOND * seconds

        for t in self.children:

            energy += t.energy_needed()

        return energy

    def eat(self, available_water, seconds):
        """
        a trunk can eat water_needed_by_trunk() units of water per second;
        if its energy is already full the plant does not eat any food
        returns the amount of food eaten by this trunk and its children
        """

        if available_water <= 0:

            return 0

        water_needed = 0

        if self.energy < 1.0:

            #a trunk can eat Trunk.MAX_FOOD_INTAKE_ONE_SECOND per second at most
            usable_water = Trunk.MAX_FOOD_INTAKE_ONE_SECOND * seconds

            if usable_water > available_water:
                usable_water = available_water

            #the amount of water needed to set the trink's energy to 1.0
            length_to_water = self.current_length * Trunk.TRUNK_LENGTH_TO_WATER_NEEDS
            #the amount of water really needed by the plant to reach energy=1.0
            water_needed = (1.0 - self.energy) * length_to_water

            if water_needed > usable_water:
                water_needed = usable_water

            #energy to be added to this trunk
            e = water_needed / length_to_water

            self.energy += e

            #some safety clamping
            if self.energy > 1.0:

                print("this shouldn't be happening...")
                self.energy = 1.0

            #remove the used water from the reserve
            available_water -= water_needed

        #feed every branch the same quantity of food
        if len(self.children) > 1:
            available_water = available_water / len(self.children)

        for t in self.children:

            water_needed += t.eat(available_water, seconds)

        return water_needed

    def keep_alive(self, seconds):

        """
        try to keep alive the trunk and its childs
        returns the energy consumed by this trunk and all its children
        """

        consumed_energy = Trunk.ENERGY_NEEDED_TO_LIVE_ONE_SECOND * seconds

        self.energy -= consumed_energy

        for t in self.children:

            consumed_energy += t.keep_alive(seconds)

        return consumed_energy

    def grow(self, seconds):
        """
        a trunk can grow a max of Trunk.MAX_GROW_UNIT_ONE_SECOND centimeters
        per second
        """
        for n in self.children:

            n.grow(seconds)

        energy_needed = Trunk.ENERGY_NEEDED_TO_GROW_ONE_SECOND * seconds

        #verify that this trunk has the energy needed to grow
        if self.energy >= energy_needed:

            #varify that this trunk has not reached its maximum length
            if self.current_length < self.max_length:

                self.energy -= energy_needed

                self.current_length += self.max_grow_unit_one_second * seconds

                if self.current_length > self.max_length and len(self.children) <= 0:

                    self.current_length = self.max_length

                    self.children.extend(Trunk.next_children(self.type, self.max_length))

    def serialize(self):

        children = [c.serialize() for c in self.children]

        obj = {'node_type': self.type, 'angle': self.angle,
               'length': self.current_length, 'max_length': self.max_length,
               'max_grow_unit': self.max_grow_unit,
               'energy': self.energy, 'children': children}

        return obj
