'''
Created on Aug 10, 2016

@author: Nick
'''

def multiplyTwo(var1 = 1, var2 = 1, *args):
    print("{} times 2 is {}".format(str(var1), var1 * 2))
    print("{} times 2 is {}".format(str(var2), var2 * 2))
    
    listEx = [var1 * 2, var2 * 2]
    print(listEx)
    
    for i in args:
        listEx.append(i * 2)
        
    return listEx

def howOld(age):
    if age > 35:
        return "You're older than me."
    elif age < 35:
        return "You're younger than me."
    
def animal(yourAnimal):
    animalPref = 'Same as me.' if (yourAnimal == "cat") else 'boo hiss'
    return animalPref

def divideStuff(x, y):
    try:
        divResult = x / y
    except ZeroDivisionError:
        print("Division by zero.")
    except TypeError as e:
        print("Not enough args.")
    except Exception:
        print("Something else went wrong.")
    else:
        print("{} divided by {} = {}".format(str(x), str(y), str(divResult)))
    finally:
        print("Done.")

def main():
    doubles = multiplyTwo(1, 2, 3, 4, 5,)
    print(doubles)
    
    print(howOld(36))
    
    print(animal('dog'))
    
    xIn = input("Enter x: ")
    yIn = input("Enter y: ")
    divideStuff(int(xIn), int(yIn))

if __name__ == "__main__":main()