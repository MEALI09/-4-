import numpy as np
import matplotlib.pyplot as plt

# функция
def y(x, q):
    return np.log(1 + x**q)

# метод наименьших квадратов (аппроксимация многочленом 2-й степени)
def least_squares_poly2(q, n):
    x = np.linspace(0, 1, n+1)
    y_vals = y(x, q)

    # моменты
    m0 = np.mean(x**0)
    m1 = np.mean(x**1)
    m2 = np.mean(x**2)
    m3 = np.mean(x**3)
    m4 = np.mean(x**4)

    # правые части
    K0 = np.mean(y_vals * (x**0))
    K1 = np.mean(y_vals * (x**1))
    K2 = np.mean(y_vals * (x**2))

    # система линейных уравнений
    A = np.array([
        [m0, m1, m2],
        [m1, m2, m3],
        [m2, m3, m4]
    ])
    b = np.array([K0, K1, K2])

    # решаем систему
    c = np.linalg.solve(A, b)

    return c

# === Основной запуск ===
n = 20  # число узлов (можно менять)

for q in [1, 2, 3]:
    c = least_squares_poly2(q, n)

    xs = np.linspace(0, 1, 400)
    ys = y(xs, q)
    ys_approx = c[0] + c[1]*xs + c[2]*xs**2

    plt.figure(figsize=(7,5))
    plt.plot(xs, ys, label=f"y(x)=ln(1+x^{q})", color="blue")
    plt.plot(xs, ys_approx, "--", label="Аппроксимация (МНК, m=2)", color="red")
    plt.title(f"Аппроксимация функции при q={q}, n={n}")
    plt.xlabel("x")
    plt.ylabel("y(x)")
    plt.legend()
    plt.grid(True)
    plt.show()
