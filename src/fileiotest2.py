'''
Created on Aug 8, 2016

@author: Nick
'''
bestStudent = {}
f = open('studentgrades.txt')
for line in f:
    name, grade = line.split()
    bestStudent[grade] = name
    
f.close()

bestStudentStr = ""

for i in sorted(bestStudent.keys(), reverse=True):
    print(bestStudent[i] + ' scored a ' + i)
    bestStudentStr += bestStudent[i] + ' scored a ' + i + '.\n'
    
    print(bestStudentStr)

bestStudentStr = '\nThe best students ranked\n\n' + bestStudentStr

outToFile = open('gradesranked.txt', mode='w')
outToFile.write(bestStudentStr)

outToFile.close()

print("Done.")