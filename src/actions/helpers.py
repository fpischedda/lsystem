#! /usr/bin/python

# Some helpers functions

__author__="francescopischedda"
__date__ ="$30-dic-2011 17.59.02$"

def grow(parameters):

    p = parameters['session'].user.plants[parameters['name']]

    p.grow(1.0)

    return {'result' : 'OK', 'plant': p.serialize()}

def eat(parameters):

    p = parameters['session'].user.plants[parameters['name']]

    p.eat()
    p.grow(0.5)

    return {'result' : 'OK', 'plant': p.serialize()}

if __name__ == "__main__":
    print "Hello World";
