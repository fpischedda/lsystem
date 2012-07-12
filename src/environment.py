#! /usr/bin/python

# This singleton class handles the plants and expose functions to interact
# with user actions

__author__="francescopischedda"
__date__ ="$30-dic-2011 17.15.22$"

from plant import Plant
import datetime

class Environment:

    LIGHTS_ON_GROW_SCALE = 0.1
    LIGHTS_OFF_GROW_SCALE = 1.0

    @classmethod
    def unserialize(cls, obj):

        e = cls(obj['name'], obj['light_on'], obj['light_off'])
        e.updated_at = obj['updated_at']

        for p in obj['plants']:
            e.plants[p["name"]] = Plant.unserialize(p)

        return e


    def __init__(self, name, light_on=5, light_off=21):

        self.name = name
        self.plants = {}
        self.light_on = light_on
        self.light_off = light_off

        self.light_hours = self.light_off - self.light_on
        self.dark_hours = 24 - self.light_hours
        
        self.updated_at = datetime.datetime.now()

    def add_plant(self, p):

        self.plants[p.name] = p
        
    def add_water(self, plant_name, liters):

        return self.plants[plant_name].fill_water(float(liters))

    def grow_plant(self, plant_name, seconds):

        self.plants[plant_name].grow(seconds)

        return 0

    def update_all_plants(self, seconds, lights_on):

        if lights_on:
            for v in self.plants.values():

                v.light_on_cycle(seconds)
        else:
            for v in self.plants.values():

                v.light_off_cycle(seconds)

    def update(self, now):

        time_diff = now - self.updated_at
        updated_at = self.updated_at

        zero = datetime.timedelta(microseconds=0)
        while time_diff > zero:
            print time_diff

            ligths_on = datetime.datetime(updated_at.year,updated_at.month, updated_at.day, self.light_on)
            ligths_off = datetime.datetime(updated_at.year,updated_at.month, updated_at.day, self.light_off)

            light_on_diff = updated_at - ligths_on
            light_off_diff = updated_at - ligths_off

            #check if the last update has finished somewhere in the lights off cycle
            if light_on_diff < zero:

                on_flag = False
                update_time = -light_on_diff

            elif light_off_diff < zero:
                #the last update finished somewhere in the lights on cycle
                #try to update time of the whole lights on cycle
                on_flag = True
                update_time = -light_off_diff

            else:
                #updating in the middle of the light off period
                on_flag = False
                update_time = datetime.timedelta(hours=self.dark_hours) - light_off_diff

            if update_time > time_diff:
                    update_time = time_diff

            self.update_all_plants(update_time.seconds, on_flag)

            time_diff -= update_time
            updated_at += update_time

        self.updated_at = now

    def serialize(self):

        plants = [p.serialize() for p in self.plants.values()]
        return {
            'name':self.name,
            'light_on':self.light_on,
            'light_off':self.light_off,
            'updated_at':self.updated_at,
            'plants':plants}

if __name__ == "__main__":

    e = Environment('test')

    print e

    ser = e.serialize()
    print ser

    ee = Environment.unserialize(ser)
    print ee.name

    ee.update(datetime.datetime.now())