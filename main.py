import math
import numpy as np
import matplotlib.pyplot as plt

# параметры
n = 10   # число узлов
j = 2
k = 1
m = 1

# функция f(x)
def f(x):
    return 1 - x**j - math.tan((math.pi * x**m) / 4)**k

# узлы и значения
x_nodes = np.arange(n+1)   # точки i = 0,...,n
values = [f(i) for i in x_nodes]

# 1) максимум и его индекс
f_max = max(values)
i_max = values.index(f_max)

# 2) минимум
f_min = min(values)

# 3) среднее, средний квадрат, среднеквадратичное значение
f_mean = np.mean(values)
f_mean_square = np.mean([v**2 for v in values])
f_rms = math.sqrt(f_mean_square)

# 4) относительное число положительных и отрицательных
n_plus = sum(1 for v in values if v > 0)
n_minus = sum(1 for v in values if v < 0)
p_plus = n_plus / (n+1)
p_minus = n_minus / (n+1)

# 5) среднеквадратичное отклонение от среднего
std_dev = math.sqrt(np.mean([(v - f_mean)**2 for v in values]))

# вывод чисел
print("Значения функции:", values)
print("Максимум =", f_max, "в узле i =", i_max)
print("Минимум =", f_min)
print("Среднее значение =", f_mean)
print("Средний квадрат =", f_mean_square)
print("Среднеквадратичное значение =", f_rms)
print("Относительное число положительных =", p_plus)
print("Относительное число отрицательных =", p_minus)
print("СКО от среднего =", std_dev)

# === ГРАФИК ===
plt.figure(figsize=(8,5))
plt.plot(x_nodes, values, marker='o', linestyle='-', color='b', label="f(x)")

# подписи точек
for i, v in zip(x_nodes, values):
    plt.text(i, v, f"{v:.2f}", fontsize=9, ha='center', va='bottom')

# выделим минимум и максимум
plt.scatter(i_max, f_max, color='red', s=80, label="Максимум")
plt.scatter(values.index(f_min), f_min, color='green', s=80, label="Минимум")

plt.axhline(y=f_mean, color='orange', linestyle='--', label="Среднее")
plt.title("График функции f(x)")
plt.xlabel("i (узлы)")
plt.ylabel("f(i)")
plt.legend()
plt.grid(True)
plt.show()
