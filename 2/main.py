from numpy import linspace
from sympy import Interval, Symbol
from sympy.calculus.util import minimum
from random import randrange
import matplotlib.pyplot as plt

k, g = 9.0, 6.0

error = 0.01


def func(x): return x ** 2 + 2 * k * g * x + k


def borders(): return -k*g-2, k*g+1


def dividing_min():
    a, b = borders()
    while True:
        x_m = (a + b) / 2
        l = b - a
        x1 = a + l/4
        x2 = b - l/4
        if func(x1) < func(x_m):
            b = x_m
            x_m = x1
            l = b - a
            if abs(l) < error:
                return x_m
        else:
            if func(x2) < func(x_m):
                a = x_m
                x_m = x2
                l = b - a
                if abs(l) < error:
                    return x_m
            else:
                a = x1
                b = x2
                l = b - a
                if abs(l) < error:
                    return x_m


def random_min():
    return min([func(randrange(int(-k*g-2), int(k*g+1))) for _ in range(100)])


def exact_value():
    a, b = borders()
    x = Symbol('x')
    return minimum(x ** 2 + 2 * k * g * x + k, x, Interval(a, b))


def plot_image():
    a, b = borders()
    x = linspace(a, b)
    plt.figure()
    plt.title('Dependence: f(x) = x^2 + 108x + 9')
    plt.plot(x, func(x))
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid()
    plt.show()


def main():
    div = float('{:.3f}'.format(func(dividing_min())))
    ex = float('{:.3f}'.format(exact_value()))
    rand = float('{:.3f}'.format(random_min()))
    print('{:<12}{:<20}{:<12}{:<16}'.format('RESULTS', 'Interval division', 'Exactly', 'Difference'))
    print('{:<12}{:<20}{:<12}{:<16}'.format('', div, ex, float('{:.3f}'.format(abs(div-ex)))), '\n')
    print('{:<12}{:<20}{:<12}{:<16}'.format('RESULTS', 'Random find', 'Exactly', 'Difference'))
    print('{:<12}{:<20}{:<12}{:<16}'.format('', rand, ex, float('{:.3f}'.format(abs(rand-ex)))))
    plot_image()


main()
