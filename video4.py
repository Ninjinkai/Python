# Tuples, lists, dictionaries

tupleEx = ('Nick', 35, 'Florida')

for i in tupleEx:
    print(i)

listEx = ['Nick', 35, 'Florida']
listEx.append(13)
listEx.remove('Florida')
listEx.insert(1, 'Petty')

for i in listEx:
    print(i)

dictEx = ({'Age':35,'Height':188,'Weight':75})
print(dictEx)
print(dictEx['Height'])

for i in [1,3,5,7,9]:
    print(i+1)

listCycle = []
listCycle[:] = range(1,20)
for i in listCycle: print(i/2)

newListCycle = range(1, 10)
for i in newListCycle: print(-i)
