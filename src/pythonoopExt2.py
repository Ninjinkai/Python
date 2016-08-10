'''
Created on Aug 9, 2016

@author: Nick
'''
from pythonoop import Animal, talkToMe
from pythonoopExt import Dog
class Cat(Animal):
    def noise(self):
        print("meow")
       
jake = Dog() 
sophie = Cat()
thing = Animal()

talkToMe(sophie)
talkToMe(jake)
talkToMe(thing)

sophie.set_attributes("fur", "fluffy")
jake.set_attributes("fur", "short")

print(sophie.get_attributes("fur"))
print(jake.get_attributes("fur"))
print(thing.get_attributes("fur"))