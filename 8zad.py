import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------
# Вариант 4: f(x) = 1 / |3 + 2cos(x/2)| , a=0, b=π
# ---------------------------------------------
def f(x):
    return 1 / np.abs(3 + 2 * np.cos(x / 2))

a = 0
b = np.pi
n = 50  # число узлов

x = np.linspace(a, b, n + 1)
y = f(x)

# Метод прямоугольников
dx = (b - a) / n
I_rect = np.sum(f(x[:-1])) * dx

# Метод трапеций
I_trap = (dx / 2) * np.sum(f(x[:-1]) + f(x[1:]))

# Метод Симпсона
if n % 2 == 1:
    n += 1
    x = np.linspace(a, b, n + 1)
    y = f(x)
dx = (b - a) / n
I_simp = (dx / 3) * (y[0] + 4 * np.sum(y[1:n:2]) + 2 * np.sum(y[2:n-1:2]) + y[n])

# Вывод результатов
print(f"Метод прямоугольников: {I_rect:.6f}")
print(f"Метод трапеций:       {I_trap:.6f}")
print(f"Метод Симпсона:       {I_simp:.6f}")

# ---------------------------------------------
# График функции и приближений
# ---------------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(x, y, label='f(x)')
plt.fill_between(x[:-1], 0, y[:-1], alpha=0.2, label='Метод прямоугольников')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Численное интегрирование: методы прямоугольников, трапеций, Симпсона')
plt.legend()
plt.grid(True)
plt.show()
