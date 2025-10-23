import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -----------------------------
# Параметры эллипсоида
# -----------------------------
a1, a2, a3 = 3.0, 2.0, 1.5  # полуоси эллипсоида

# -----------------------------
# Параметры функции ρ(x)
# -----------------------------
alpha = np.random.uniform(-5, 5, 3)
beta = np.random.uniform(0.5, 4, 3)
p = np.random.uniform(0.1, 0.5, 3)
q = np.random.uniform(0.1, 2, 3)
N = 2  # степень в экспоненте

# -----------------------------
# Функция плотности
# -----------------------------
def rho(x):
    val = 1.0
    for i in range(3):
        val *= abs(x[i] - alpha[i])**beta[i] * np.exp(-p[i] * abs(x[i] - q[i])**N)
    return val

# -----------------------------
# Проверка принадлежности точке области эллипсоида
# -----------------------------
def inside_ellipsoid(x):
    return (x[0]**2 / a1**2 + x[1]**2 / a2**2 + x[2]**2 / a3**2) <= 1.0

# -----------------------------
# Метод Монте-Карло
# -----------------------------
N_points = 100_000  # общее число случайных точек
count_inside = 0
sum_rho = 0.0

# Параллелепипед, в который вписан эллипсоид
xmin, xmax = -a1, a1
ymin, ymax = -a2, a2
zmin, zmax = -a3, a3
W_volume = (xmax - xmin) * (ymax - ymin) * (zmax - zmin)

# Генерация случайных точек
points = np.random.uniform([xmin, ymin, zmin], [xmax, ymax, zmax], size=(N_points, 3))

# Массивы для графика
inside_points = []
outside_points = []

for x in points:
    if inside_ellipsoid(x):
        count_inside += 1
        sum_rho += rho(x)
        inside_points.append(x)
    else:
        outside_points.append(x)

inside_points = np.array(inside_points)
outside_points = np.array(outside_points)

# -----------------------------
# Вычисление интеграла
# -----------------------------
V_est = W_volume * count_inside / N_points  # объем области
I_est = V_est * (sum_rho / count_inside)    # интеграл

# -----------------------------
# Вывод результатов
# -----------------------------
print("α =", alpha)
print("β =", beta)
print("p =", p)
print("q =", q)
print(f"Приближённый объём области V = {V_est:.5f}")
print(f"Оценка интеграла I = {I_est:.5f}")

# -----------------------------
# Построение 3D-графика
# -----------------------------
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Точки внутри эллипсоида — зелёные
if len(inside_points) > 0:
    ax.scatter(inside_points[:, 0], inside_points[:, 1], inside_points[:, 2],
               color='green', s=2, label='Внутри области V')

# Точки вне эллипсоида — красные
if len(outside_points) > 0:
    ax.scatter(outside_points[:, 0], outside_points[:, 1], outside_points[:, 2],
               color='red', s=1, alpha=0.3, label='Вне области V')

# Отрисовка границы эллипсоида
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(0, np.pi, 30)
x = a1 * np.outer(np.cos(u), np.sin(v))
y = a2 * np.outer(np.sin(u), np.sin(v))
z = a3 * np.outer(np.ones_like(u), np.cos(v))
ax.plot_surface(x, y, z, color='cyan', alpha=0.2)

ax.set_xlabel("x₁")
ax.set_ylabel("x₂")
ax.set_zlabel("x₃")
ax.set_title("Метод Монте-Карло — интегрирование по эллипсоиду")
ax.legend()
plt.tight_layout()
plt.show()
