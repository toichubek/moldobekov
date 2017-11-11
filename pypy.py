# -*- coding: utf-8 -*-
import math
import matplotlib.pyplot as plt
phi = lambda y: math.e ** (-math.e ** (-y))

def yt(y):
    e = math.e; log = math.log
    slag1 = -log(-log(y))/log(e, 10)
    slag2 = -log(log(e, 10), 10)/log(e, 10)
    return round(slag1+slag2, 3) 

x_list = []
with open('table4') as fin:
    for line in fin:
        year, x = line.split(' ')
        x_list.append(float(x.strip()))

x_list.sort()
plt_y = []
plt_x = []
plt_k = []

with open('table5', 'w') as fout:
    for k in range(1, 73):
        x = x_list[k]
        kn = round(k/73, 3)
        y = phi(kn)
        yk = yt(y)#;
        line = '{0} {1} {2} {3}\n'.format(k,kn,yk,x)
        fout.write(line)
        plt_y.append(yk)
        plt_k.append(kn)
        plt_x.append(x)

plt_x = list(map(lambda x: x*1000, plt_x))

x_average = sum(plt_x)/len(plt_x)

x2 = sum(x*x for x in plt_x)
x1 = sum(plt_x)
x3 = (x1**2)/72
sx = ((x2-x3)/72)**(1/2)

Yn, Tn = 0, 0
with open('table2') as fin:
    for line in fin:
        N, yn, tetan = line.split(' ')
        if int(N) == len(plt_x):
            Yn = float(yn)
            Tn = float(tetan)
            break

al = sx / Tn
ql = x_average - al*Yn
print('al',al, ql)

plx = lambda y: al*y + ql
ply = lambda x: (x - ql)/al

def plotting():
    y = range(-200, 600)
    y = list(map(lambda x: x/100, y))
    xx=list(map(phi, y))
    x = range(0, 10000)
    x = list(map(lambda s: s/100, x))
    ax=plt.axes()
    ax.plot(list(map(plx, y)), xx,'b--', plt_x, plt_k, 'ro')
    ax2=ax.twinx()
    ax2.plot(list(map(plx, y)), phi(y),'b--', plt_x, plt_k, 'ro')
      #  plt.plot(list(map(plx, y)), phi(y), plt_x, plt_k, 'ro')

    plt.axis([4000, 17000, -0.05, 1.05])
    plt.ylabel('закон распределения')
    plt.xlabel('max water consumption m^3/sec')
    plt.show()

plotting()