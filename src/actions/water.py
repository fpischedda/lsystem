#! /usr/bin/python

# plant related actions

__author__="francescopischedda"
__date__ ="$30-dic-2011 17.01.48$"

def add_water(parameters):
    """
    try to use the requested liters of water from the water-reserve item
    the liters cannot be more than what the pot can handle
    the liters cannot be more than what is available in the water-reserve item
    return the amount of water in the pot and the remaining water
    in the water-reserve
    """
    u = parameters['session'].user
    p = u.plants[parameters['name']]

    max_water = p.pot_water_capacity - p.available_water

    liters = parameters['liters']
    if liters > max_water:
        liters = max_water

    usable_water = u.use_item('water-reserve', liters)
    available_water = p.add_water(usable_water)
    
    return {'result' : 'OK', 
        'available_water':available_water,
        'water-reserve':u.items['water-reserve'].quantity}

if __name__ == "__main__":
    print "Hello World";
