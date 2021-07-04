a = '123\t1\n456\t2\n\t3\n\n\n'
print(a)
b = a.split('\n')
print(b)

l1=[]
l2=[]
combos=''

for i in b:
    t = i.split('\t')
    print(t)
    if len(t) == 1 : break
    if t[0] != '' : l1.append(t[0])
    if t[1] != '' : l2.append(t[1])

for i in l1:
    for j in l2:
        combos += i + '\t' + j + '\n'
print(combos)