# Strings

stringVar = "This is a string."
print(stringVar)

num1 = 3
word1 = "cats"

print("I have {} {}.".format(num1, word1))
print("I have {} {}.".format(num1, word1).find('have'))
print("I have {} {}.".format(num1, word1).replace('cats', 'dogs'))

newString = "I have " + str(num1) + ' ' + word1 +"."
print(newString)
