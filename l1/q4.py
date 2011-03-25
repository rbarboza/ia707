import pylab
from math import pow
import psyco
psyco.full()




def fact(x):
    if x < 2:
        return 1
    else:
        return x*fact(x-1)

def fact_2(x,y):
    if x < 2:
        return 1
    elif x == y:
        return y
    else:
        return x*fact_2(x-1, y)


def binom(n,k):
    return fact_2(n,n-k+1)/fact(k)

def f(n,k):
    sum = 0
    for i in xrange(k+1):
        sum += pow(-1,i) * binom(k,i)*pow((k-i),n)

    return int(sum) / fact(k)

y = [f(25,k) for k in range(20)]
x = range(20)

pylab.plot(x,y)
pylab.xlabel("k")
pylab.ylabel("f(25,k)")
pylab.show()

y = [f(n,10) for n in range(25)]
x = range(25)

pylab.plot(x,y)
pylab.xlabel("n")
pylab.ylabel("f(n,10)")
pylab.show()
