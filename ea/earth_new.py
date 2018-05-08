# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 20:01:02 2018

@author: TOICHUBEK
"""


import math
import matplotlib.pyplot as plt
phi = lambda y: math.e ** (-math.e ** (-y))
 # phi формула закона распределения для нормированных значений у


dlina=99      # РАЗМЕРНОСТЬ ДАННЫХ

def yt(y):   # значения у(k)  формула (10.5.21)
    e = math.e; log = math.log
    slag1 = -log(-log(y))/log(e, 10)
    slag2 = -log(log(e, 10), 10)/log(e, 10)
    return round(slag1+slag2, 3) 

x_list = []
with open('earth') as fin:     #  таблица №4 из книги МАХ расходы по годам
    for line in fin:
        year, x = line.split('\t')
        x_list.append(float(x.strip()))

x_list.sort()   # сортировка расходов по увеличении
plt_y = []
plt_x = []
plt_k = []

with open('earth_table_k', 'w') as fout:      #  таблица №5 из книги
    for k in range(1, dlina):
        x = x_list[k]            # 4-столбец   x расходы воды в 1000м3
        kn = round(k/dlina, 3)      # 2-столбец   к/(N+1)
        y = phi(kn)
        yk = yt(y)              # 3-столбец  нормированные у(к)
        line = '{0} {1} {2} {3}\n'.format(k,kn,yk,x)
        fout.write(line)
        plt_y.append(yk)
        plt_k.append(kn)
        plt_x.append(x)

plt_x = list(map(lambda x: x*1000, plt_x))  # тысяча м3 -> м3

x_average = sum(plt_x)/len(plt_x)    #  средний арифметический наблюдений

x2 = sum(x*x for x in plt_x)
x1 = sum(plt_x)
x3 = (x1**2)/(dlina-1)
sx = ((x2-x3)/(dlina-1))**(1/2)    #  средний квадратический наблюдений

Yn, Tn = 0, 0
with open('table2') as fin:   #  таблица №2  средние значения у(к)
    for line in fin:
        N, yn, tetan = line.split(' ')
        if int(N) == len(plt_x):
            Yn = float(yn)         #  средний арифметический из таблицы
            Tn = float(tetan)        #  средний квадратический
            break

al = sx / Tn              #  параметр 1/a
ql = x_average - al*Yn      #  параметр q для максимума
print('\n уравнение прямой : y={0}x+{1}\n'.format( round(al),round(ql) ))

plx = lambda y: al*y + ql        
ply = lambda x: (x - ql)/al

def plotting():
    y = list(map(lambda x:x/100, range(-220, 700)))
    ax=plt.axes()
    plt.xlabel('max water consumption m^3/sec')
    plt.ylabel('нормированные значения')
    ax.plot(list(map(plx, y)), y)   # синий график уравнения 
    ax2=ax.twinx()
    plt_y=list(map(lambda x: math.log(x,math.exp(0.1)),plt_k))
    ax2.plot(plt_x, plt_y, 'ro')   # красные точки наблюдений
    ax2.set_yscale('symlog',linthreshy=0.9)
    ax.grid(color = 'k')                  # черная сетка графика
    plt.axis([12000, 19000, -165, 1.5])
    plt.ylabel('закон распределения')

    plt.show()

plotting()