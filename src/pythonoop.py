'''
Created on Aug 9, 2016

@author: Nick
'''

class Animal:
    def __init__(self, **kwargs):
        self._attributes = kwargs
        
    def set_attributes(self, key, value):
        self._attributes[key] = value
        
    def get_attributes(self, key):
        return self._attributes.get(key, None)
    
    def noise(self):
        print('Errrrr')
        
    def move(self):
        print('Moving Forward')
    
    def eat(self):
        print('Crunch, Crunch')
        
def talkToMe(Animal):
    Animal.noise()
    Animal.eat()

