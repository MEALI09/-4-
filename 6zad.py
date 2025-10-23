import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------
# Вариант 4: f(x) = 1 / |3 + 2cos(x/2)| , a=0, b=π
# ---------------------------------------------
def f(x):
    return 1 / np.abs(3 + 2 * np.cos(x / 2))

a = 0
b = np.pi
n = 50  # число узлов для метода прямоугольников (можно менять)

# ---------------------------------------------
# Метод прямоугольников
# ---------------------------------------------
def rectangle_method(f, a, b, n):
    h = (b - a) / n
    result = 0
    xs, ys = [], []
    for i in range(n):
        xi = a + (i + 0.5) * h
        result += f(xi)
        xs.append(xi)
        ys.append(f(xi))
    return result * h, xs, ys

# ---------------------------------------------
# Метод Гаусса (m = 5)
# ---------------------------------------------
def gauss_method(f, a, b, m=5):
    # Узлы и веса из методички
    t = np.array([0.046910077, 0.230765345, 0.5, 0.769234655, 0.953089923])
    A = np.array([0.118463443, 0.239314335, 0.284444444, 0.239314335, 0.118463443])

    result = 0
    for i in range(m):
        x = a + (b - a) * t[i]
        result += A[i] * f(x)
    result *= (b - a)
    return result

# ---------------------------------------------
# Вычисления
# ---------------------------------------------
I_rect, xs, ys = rectangle_method(f, a, b, n)
I_gauss = gauss_method(f, a, b)

# ---------------------------------------------
# Вывод результатов
# ---------------------------------------------
print("=== ЧИСЛЕННОЕ ИНТЕГРИРОВАНИЕ (Вариант 4) ===")
print(f"Метод прямоугольников ({n} узлов): {I_rect:.6f}")
print(f"Метод Гаусса (m=5): {I_gauss:.6f}")

# ---------------------------------------------
# Сохранение в Excel
# ---------------------------------------------
df = pd.DataFrame({
    "x": xs,
    "f(x)": ys
})
df.loc[len(df.index)] = ["Интеграл (прямоугольники)", I_rect]
df.loc[len(df.index)] = ["Интеграл (Гаусс)", I_gauss]
df.to_excel("integral_variant4.xlsx", index=False)
print("\nРезультаты сохранены в файл integral_variant4.xlsx")

# ---------------------------------------------
# График функции и прямоугольников
# ---------------------------------------------
x_plot = np.linspace(a, b, 500)
y_plot = f(x_plot)

plt.figure(figsize=(10, 6))
plt.plot(x_plot, y_plot, 'b-', label='f(x)')
plt.bar(xs, ys, width=(b - a) / n, alpha=0.3, color='orange', align='center', label='Прямоугольники')
plt.title("Численное интегрирование — Вариант 4")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()
