'''
Created on Aug 8, 2016

@author: Nick
'''
bestGrade = 0
f = open('studentgrades.txt')
for line in f:
    name, grade = line.split()
    if int(grade) > bestGrade:
        bestGrade = int(grade)
        bestStudent = name

print('Best Grade: ', bestGrade)
print('Best Student: ', bestStudent)

f.close()