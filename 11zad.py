import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Вариант 4: функция f(x, y)
# -------------------------------
m = 2
n = 1

def f(x, y):
    # Защита от выхода за область определения arcsin(|x|^m)
    if abs(x)**m > 1 or abs(y)**m > 1:
        return np.inf
    return (np.arcsin(abs(x)**m) + np.arcsin(abs(y)**m)) / (2**n)

# -------------------------------
# Начальные параметры
# -------------------------------
a = 0.5
b = 0.7
beta = 0.5
eps = 1e-4
kmax = 50

d = np.sqrt(a**2 + b**2)
alpha = np.sqrt(1 - beta**2)

x = a
y = b
print(f"Начальные данные: a={a}, b={b}, β={beta}, d={d:.3f}")

# -------------------------------
# Метод золотого сечения
# -------------------------------
def golden_section_search(func, a, b, tol=1e-5):
    gr = (np.sqrt(5) + 1) / 2
    c = b - (b - a) / gr
    d = a + (b - a) / gr
    while abs(c - d) > tol:
        if func(c) < func(d):
            b = d
        else:
            a = c
        c = b - (b - a) / gr
        d = a + (b - a) / gr
    return (b + a) / 2

# -------------------------------
# Координатный спуск
# -------------------------------
k = 0
delta = float('inf')
x_hist, y_hist = [x], [y]

while delta > eps and k < kmax:
    # Минимизация по x
    def fx(x_val): return f(x_val, y)
    x_new = golden_section_search(fx, -d, d)

    # Минимизация по y
    def fy(y_val): return f(x_new, y_val)
    y_new = golden_section_search(fy, -d, d)

    delta = np.sqrt((x_new - x)**2 + (y_new - y)**2)
    x, y = x_new, y_new
    k += 1

    x_hist.append(x)
    y_hist.append(y)

    print(f"{k:2d}) x={x:.6f}, y={y:.6f}, f={f(x, y):.6f}, Δ={delta:.2e}")

print("\nРезультаты:")
print(f"Минимум найден при x={x:.6f}, y={y:.6f}, f(x,y)={f(x,y):.6f}, за {k} итераций")

# -------------------------------
# Визуализация
# -------------------------------
X = np.linspace(-1, 1, 200)
Y = np.linspace(-1, 1, 200)
X, Y = np.meshgrid(X, Y)
Z = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        try:
            Z[i, j] = f(X[i, j], Y[i, j])
        except:
            Z[i, j] = np.nan

plt.figure(figsize=(7, 5))
plt.contour(X, Y, Z, levels=30)
plt.plot(x_hist, y_hist, 'r.-', label='Траектория спуска')
plt.scatter(x_hist[-1], y_hist[-1], color='red', label='Минимум')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Метод координатного спуска (Вариант 4)')
plt.legend()
plt.grid(True)
plt.show()
