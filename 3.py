import math
import numpy as np
import matplotlib.pyplot as plt

# параметры функции
k = 2  # степень cos
m = 2  # показатель в корне


def y(x):
    return math.cos(math.pi * (x ** (1 / m))) ** k


# интерполяция Ньютона 2-го порядка
def newton2_interpolation(x_nodes, y_nodes, x):
    n = len(x_nodes) - 1
    h = x_nodes[1] - x_nodes[0]

    # находим индекс ближайшего узла
    j = int((x - x_nodes[0]) / h)
    if j >= n:
        j = n - 1

    p = (x - x_nodes[j]) / h

    # разности
    dy1 = y_nodes[j + 1] - y_nodes[j]
    dy2 = y_nodes[j + 2] - 2 * y_nodes[j + 1] + y_nodes[j] if j + 2 <= n else 0

    return y_nodes[j] + p * dy1 + (p * (p - 1) / 2) * dy2


# функция оценки погрешностей
def analyze(n):
    x_nodes = np.linspace(0, 1, n + 1)
    y_nodes = [y(x) for x in x_nodes]

    errors = []
    x_mid = []
    for j in range(n):
        x_half = x_nodes[j] + 0.5 * (1 / n)
        exact = y(x_half)
        interp = newton2_interpolation(x_nodes, y_nodes, x_half)
        errors.append(abs(exact - interp))
        x_mid.append(x_half)

    e_max = max(errors)
    e_sq = np.mean([e ** 2 for e in errors])
    e_m = math.sqrt(e_sq)
    return e_max, e_m, x_nodes, y_nodes, x_mid, errors


# исследование для разных n
results = {}
for n in [4, 8, 16, 32]:
    e_max, e_m, x_nodes, y_nodes, x_mid, errors = analyze(n)
    results[n] = (e_max, e_m, x_nodes, y_nodes, x_mid, errors)
    print(f"n={n}: ε_max={e_max:.3e}, ε_m={e_m:.3e}")

# === ГРАФИКИ ===

# 1. Сравнение функции и интерполяции при n=16
n = 16
_, _, x_nodes, y_nodes, _, _ = results[n]

xs = np.linspace(0, 1, 400)
ys = [y(x) for x in xs]
ys_interp = [newton2_interpolation(x_nodes, y_nodes, x) for x in xs]

plt.figure(figsize=(8,5))
plt.plot(xs, ys, label="y(x) (точная)", color="blue")
plt.plot(xs, ys_interp, "--", label="Интерполяция Ньютона (n=16)", color="red")
plt.scatter(x_nodes, y_nodes, color="black", marker="o", label="Узлы")
plt.title("Функция и интерполяция Ньютона (2-го порядка)")
plt.xlabel("x")
plt.ylabel("y(x)")
plt.legend()
plt.grid(True)
plt.show()

# 2. Ошибки для разных n
plt.figure(figsize=(8,5))
for n in results:
    _, _, _, _, x_mid, errors = results[n]
    plt.plot(x_mid, errors, marker="o", label=f"n={n}")

plt.title("Абсолютная ошибка интерполяции Ньютона (2-го порядка)")
plt.xlabel("x (середины отрезков)")
plt.ylabel("Ошибка")
plt.yscale("log")  # логарифмическая шкала для наглядности
plt.legend()
plt.grid(True, which="both")
plt.show()
