from random import random
from sympy import diff, symbols

g, k = 6, 9
x0, y0, E = k*g+2, g-3, 0.01
x, y = symbols('x y')


def func():
    return x**2 + (y-g)**2 - 2*k*g*x + k


def func_val(x_min, y_min):
    return func().evalf(subs={x: x_min, y: y_min})


def dfxy(sym, sym_min):
    return diff(func(), sym).evalf(subs={sym: sym_min})


def grad_min():
    h = 1
    x_min, y_min = x0, y0
    while True:
        if sum([dfxy(x, x_min)**2, dfxy(y, y_min)**2]) <= E:
            return [x_min, y_min]
        x_min -= h * dfxy(x, x_min)
        y_min -= h * dfxy(y, y_min)
        h /= 2


def adapt_rand():
    h = 50
    counter = 0
    x_min, y_min = x0, y0
    f_min = func_val(x_min, y_min)
    while True:
        if counter > 10:
            h /= 2
            counter = 0
        e_x = random()*2-1
        e_y = (1 - e_x**2)**(1/2) * (-1)**int(random()*10)
        x_m = x_min + h * e_x
        y_m = y_min + h * e_y
        f = func_val(x_m, y_m)
        if f_min > f:
            x_m += h * e_x
            y_m += h * e_y
            f = func_val(x_m, y_m)
            if f_min > f:
                x_min = x_m
                y_min = y_m
                f_min = f
            else:
                counter += 1
        else:
            counter += 1
        if h <= E:
            return [x_min, y_min, f_min]


def main():
    res = grad_min()
    print('Gradient method with dividing the step in half:', '\n', 'X_min:', res[0],
          '; Y_min:', res[1], '; F_min:', func_val(res[0], res[1]))
    res = adapt_rand()
    print('Adaptive method of random search:', '\n', 'X_min:', res[0],
          '; Y_min:', res[1], '; F_min:', res[2])


main()
