# -*- coding=utf-8 -*-

f = open('/media/alex/DATA/pass.txt')
f1 = open('/media/alex/DATA/passes.txt', 'w')
for z in f:
    i = 0
    ar = []
    while i < len(z):
        if z[i] == '\t':
            ar.append(i)
        i += 1
    f1.write(z[ar[0]+1:ar[1]] + '\n')
