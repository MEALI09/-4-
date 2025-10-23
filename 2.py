import math
import matplotlib.pyplot as plt
import numpy as np

# Параметры функции (можешь менять 1..4)
j = 2
k = 1
m = 1

# Функция f(x)
def f(x):
    theta = math.pi * (x**m) / 4.0
    return 1 - x**j - (math.tan(theta) ** k)

# Производная f'(x) для метода Ньютона
def fprime(x):
    theta = math.pi * (x**m) / 4.0
    dtheta_dx = (math.pi * m * (x**(m-1))) / 4.0 if not (x==0 and m>1) else 0.0
    tan_theta = math.tan(theta)
    sec2 = 1.0 / (math.cos(theta)**2)
    deriv_tank = k * (tan_theta**(k-1)) * sec2 * dtheta_dx if k != 0 else 0.0
    return - j * (x**(j-1)) - deriv_tank

# Поиск интервала
def find_bracket(func, a=0.0, b=1.0, samples=200):
    fa = func(a); fb = func(b)
    if fa * fb <= 0:
        return a, b
    xs = [a + (b-a)*i/samples for i in range(samples+1)]
    fs = [func(x) for x in xs]
    for i in range(samples):
        if fs[i] * fs[i+1] <= 0:
            return xs[i], xs[i+1]
    raise ValueError("Не найден интервал с изменением знака на [0,1]")

# Метод бисекции
def bisection(func, a, b, tol=1e-8, max_iter=100):
    fa = func(a); fb = func(b)
    if fa * fb > 0:
        raise ValueError("Нет изменения знака на концах отрезка")
    it = 0
    while (b - a) / 2.0 > tol and it < max_iter:
        c = (a + b) / 2.0
        fc = func(c)
        if abs(fc) < 1e-15:
            return c, fc, it+1
        if fa * fc <= 0:
            b = c; fb = fc
        else:
            a = c; fa = fc
        it += 1
    c = (a + b) / 2.0
    return c, func(c), it

# Метод секущих
def secant(func, x0, x1, tol=1e-8, max_iter=100):
    f0 = func(x0); f1 = func(x1)
    it = 0
    while it < max_iter and abs(x1 - x0) > tol:
        if f1 == f0:
            break
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, x1 = x1, x2
        f0, f1 = f1, func(x1)
        it += 1
    return x1, f1, it

# Метод Ньютона
def newton(func, dfunc, x0, tol=1e-8, max_iter=100):
    x = x0
    it = 0
    while it < max_iter:
        fx = func(x)
        dfx = dfunc(x)
        if abs(dfx) < 1e-14:
            break
        x_new = x - fx / dfx
        if abs(x_new - x) < tol:
            return x_new, func(x_new), it+1
        x = x_new
        it += 1
    return x, func(x), it

# === Выполнение ===
a, b = find_bracket(f, 0.0, 1.0, samples=200)
print("Найден интервал:", a, b)

root_bisect, val_bisect, it_bisect = bisection(f, a, b, tol=1e-12, max_iter=200)
root_secant, val_secant, it_secant = secant(f, a, b, tol=1e-12, max_iter=200)
root_newton, val_newton, it_newton = newton(f, fprime, (a+b)/2.0, tol=1e-12, max_iter=200)

print("Бисекция:    root = {:.15f}, f(root) = {:.3e}, iter = {}".format(root_bisect, val_bisect, it_bisect))
print("Секущие:     root = {:.15f}, f(root) = {:.3e}, iter = {}".format(root_secant, val_secant, it_secant))
print("Ньютон:      root = {:.15f}, f(root) = {:.3e}, iter = {}".format(root_newton, val_newton, it_newton))
print("Контроль: f(0) = {:.6e}, f(1) = {:.6e}".format(f(0.0), f(1.0)))

# === ГРАФИК ===
xs = np.linspace(0, 1, 400)
ys = [f(x) for x in xs]

plt.figure(figsize=(8,5))
plt.axhline(0, color="black", linestyle="--", linewidth=1)

# График функции
plt.plot(xs, ys, label="f(x)", color="blue")

# Отмечаем корни
plt.scatter(root_bisect, f(root_bisect), color="red", s=80, label="Бисекция")
plt.scatter(root_secant, f(root_secant), color="green", s=80, label="Секущие")
plt.scatter(root_newton, f(root_newton), color="orange", s=80, label="Ньютон")

# Подписи к точкам
plt.text(root_bisect, f(root_bisect)+0.1, "Бисекция", color="red", ha="center")
plt.text(root_secant, f(root_secant)-0.1, "Секущие", color="green", ha="center")
plt.text(root_newton, f(root_newton)+0.1, "Ньютон", color="orange", ha="center")

plt.title("График функции и найденные корни")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()
