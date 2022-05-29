#program which calculate error of Runge-Kuta and Euler methods 
from scipy.integrate import odeint
from numpy import linspace


k = 9
g = 6


def runge_kutta(funcs: list, y=None, h=0.5, a=0, b=1, delta=0.001) -> list:
    err = delta + 1
    last_res, res = None, []
    while err > delta:
        # print("step: " + str(h))
        t = a
        res.append(y)
        while t < b:
            res.append([])
            for i in range(len(funcs)):
                k = [h * funcs[i](t, *res[-2])]
                k.append(h * funcs[i](t + h / 2, *((v + k[-1] / 2) for v in res[-2])))
                k.append(h * funcs[i](t + h / 2, *((v + k[-1] / 2) for v in res[-2])))
                k.append(h * funcs[i](t + h / 2, *((v + k[-1]) for v in res[-2])))
                res[-1].append(res[-2][i] + (k[0] + 2*k[1] + 2*k[2] + k[3])/6)
            t += h
        err = error(last_res, res, delta, funcs)
        last_res = res.copy()
        res = []
        h /= 2.0
    return last_res[-1]


def euler(funcs: list, y=None, h=0.5, a=0, b=1, delta=0.01) -> list:
    err = delta + 1
    last_res, res = None, []
    while err > delta:
        # print("step: " + str(h))
        t = a
        res.append(y)
        while t < b:
            res.append([])
            for i in range(len(funcs)):
                res[-1].append(res[-2][i] + h * funcs[i](t, *res[-2]))
            t += h
        err = error(last_res, res, delta, funcs)
        last_res = res.copy()
        res = []
        h /= 2.0
    return last_res[-1]


def error(last_res, res, delta, funcs):
    if last_res is None:
        err = delta + 1
    else:
        i = 0
        err = 0
        while i < len(res)/2 and i < len(last_res):
            for j in range(len(funcs)):
                err += (abs(last_res[i][j]) - abs(res[i*2][j]))**2
            i += 1
            err /= len(last_res) * len(funcs)
    return err


def func(x, t):
    return [k * t + x[0] - x[1] + g, -x[0] + k * x[1]]


def func1(t: float, x: float, y: float) -> float:
    return k * t + x - y + g


def func2(t: float, x: float, y: float) -> float:
    return - x + k * y


euler_res = euler([func1, func2], y=[0, 0], h=1)
runge_res = runge_kutta([func1, func2], y=[0, 0], h=1)
exactly = odeint(func, [0, 0], linspace(0.0, 1.0, 11))[-1]

print('{:<12}{:<22}{:<22}{:<22}'.format('RESULTS', 'Euler', 'RungeKutta', 'Exactly'))
print('{:<12}{:<22}{:<22}{:<22}'.format('X', euler_res[0], runge_res[0], exactly[0]))
print('{:<12}{:<22}{:<22}{:<22}'.format('Y', euler_res[1], runge_res[1], exactly[1]), '\n')

print('{:<12}{:<22}{:<22}'.format('DIFFERENCE', 'Euler', 'RungeKutta'))
print('{:<12}{:<22}{:<22}'.format('X', abs(euler_res[0] - exactly[0]), abs(runge_res[0] - exactly[0])))
print('{:<12}{:<22}{:<22}'.format('Y', abs(euler_res[1] - exactly[1]), abs(runge_res[1] - exactly[1])))
