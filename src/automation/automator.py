#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="francescopischedda"
__date__ ="$11-feb-2012 19.07.34$"

import environment
import threading
import time

class Automator(threading.Thread):

    def __init__(self, thread_interval):

        threading.Thread.__init__(self)

        self.automators = [ environment.EnvironmentsAutomator()]
        self.running = True
        self.thread_interval = thread_interval
    def end(self):
        self.running = False
        
    def run(self):

        while self.running == True:

            print("updating environments %s" %( time.time()))

            for a in self.automators:

                a.update()

            time.sleep(self.thread_interval)

if __name__ == "__main__":


    a = Automator()

    print("starting thread")
    a.start()

    print("sleep")
    time.sleep(8)
    a.end()
    print("wait for thread to finish")

    a.join()

    print("end")