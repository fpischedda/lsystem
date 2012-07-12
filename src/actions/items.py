# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="francescopischedda"
__date__ ="$8-mar-2012 17.07.44$"

from messaging import timeline

def use_magic_bottle(parameters):

    u = parameters['session'].user

    result = u.use_magic_bottle(parameters['plant_name'])

    if result == 0:
        timeline.write_to_timeline('admin', "User %s has used a magic bottle on the plant %s..." % (u.username,parameters['plant_name']))
        return {'result':'OK', 'plant':u.plants[parameters['plant_name']].serialize()}

    return {'result': 'KO', 'reason':result}

def use_item(parameters):

    u = parameters['session'].user

    result = 3

    item = parameters['item_name']
    if item == 'magic-bottle':
        result = u.use_magic_bottle(parameters['plant_name'])

    if result == 0:
        timeline.write_to_timeline('admin',
            "User %s has used a %s on the plant %s..." %
            (u.username,item, parameters['plant_name']))

        quantity = u.items[item].quantity
        return {'result':'OK', 'item':{'name':item, 'quantity': quantity}, 'plant':u.plants[parameters['plant_name']].serialize()}

    return {'result': 'KO', 'reason':result}

if __name__ == "__main__":
    print "Hello World"
