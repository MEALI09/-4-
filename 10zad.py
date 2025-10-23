import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
import math


class GoldenSectionSearch:
    def __init__(self, func, a, b, epsilon=1e-6):
        self.func = func
        self.a = a
        self.b = b 
        self.epsilon = epsilon
        self.golden_ratio = (math.sqrt(5) - 1) / 2  # ≈ 0.618
        self.history = []

    def solve(self):
        a, b = self.a, self.b
        iterations = 0

        while abs(b - a) > self.epsilon and iterations < 100:
            # Вычисляем точки золотого сечения
            L = b - a
            y = b - L * self.golden_ratio
            z = a + L * self.golden_ratio

            # Вычисляем значения функции
            f_y = self.func(y)
            f_z = self.func(z)

            # Сохраняем историю для визуализации
            self.history.append({
                'iteration': iterations,
                'a': a, 'b': b, 'y': y, 'z': z,
                'f_y': f_y, 'f_z': f_z,
                'interval_length': b - a
            })

            # Выбираем новый интервал
            if f_y < f_z:
                b = z
            else:
                a = y

            iterations += 1

        # Финальное приближение
        self.min_point = (a + b) / 2
        self.min_value = self.func(self.min_point)
        return self.min_point, self.min_value


# Пример 1: Квадратичная функция
def quadratic_function(x):
    return (x - 2) ** 2 + 3


# Пример 2: Функция с несколькими экстремумами
def complex_function(x):
    return x ** 4 - 4 * x ** 2 + 2 * x + 1


# Пример 3: Тригонометрическая функция
def trig_function(x):
    return 2 * np.sin(x) + np.cos(2 * x)


# Выбираем функцию для оптимизации
target_function = quadratic_function
a, b = 0, 5  # Интервал поиска

# Создаем оптимизатор и находим минимум
optimizer = GoldenSectionSearch(target_function, a, b, epsilon=1e-6)
min_x, min_y = optimizer.solve()

print(f"Найденный минимум: x = {min_x:.6f}, f(x) = {min_y:.6f}")
print(f"Количество итераций: {len(optimizer.history)}")

# Создаем подробную визуализацию
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Подграфик 1: Функция и процесс оптимизации
x_plot = np.linspace(a, b, 1000)
y_plot = target_function(x_plot)
ax1.plot(x_plot, y_plot, 'b-', linewidth=2, label='f(x)')
ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax1.grid(True, alpha=0.3)
ax1.set_xlabel('x')
ax1.set_ylabel('f(x)')
ax1.set_title('Метод золотого сечения - Поиск минимума')

# Подграфик 2: Сходимость
ax2.grid(True, alpha=0.3)
ax2.set_xlabel('Итерация')
ax2.set_ylabel('Длина интервала')
ax2.set_title('Сходимость метода')
ax2.set_yscale('log')

# Цвета для разных итераций
colors = plt.cm.viridis(np.linspace(0, 1, len(optimizer.history)))


# Анимация процесса
def animate(i):
    ax1.clear()
    ax2.clear()

    # Первый подграфик
    ax1.plot(x_plot, y_plot, 'b-', linewidth=2, label='f(x)')
    ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.set_title('Метод золотого сечения - Поиск минимума')

    # Второй подграфик
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('Итерация')
    ax2.set_ylabel('Длина интервала')
    ax2.set_title('Сходимость метода')
    ax2.set_yscale('log')

    # Отображаем историю до текущей итерации
    for j, step in enumerate(optimizer.history[:i + 1]):
        color = colors[j]

        # Отображаем текущий интервал
        ax1.axvspan(step['a'], step['b'], alpha=0.2, color=color)
        ax1.axvline(step['a'], color=color, linestyle='--', alpha=0.7)
        ax1.axvline(step['b'], color=color, linestyle='--', alpha=0.7)

        # Отображаем точки y и z
        ax1.plot(step['y'], step['f_y'], 'ro', markersize=6, alpha=0.8)
        ax1.plot(step['z'], step['f_z'], 'go', markersize=6, alpha=0.8)

        # Добавляем текст для первых нескольких итераций
        if j < 3:
            ax1.text(step['y'], step['f_y'] + 0.5, f'y_{j}', fontsize=8)
            ax1.text(step['z'], step['f_z'] + 0.5, f'z_{j}', fontsize=8)

    # Отображаем найденный минимум
    ax1.plot(min_x, min_y, 'r*', markersize=15, label=f'Минимум: ({min_x:.4f}, {min_y:.4f})')
    ax1.legend()

    # График сходимости
    iterations = [step['iteration'] for step in optimizer.history[:i + 1]]
    intervals = [step['interval_length'] for step in optimizer.history[:i + 1]]
    ax2.plot(iterations, intervals, 'bo-', linewidth=2, markersize=4)
    ax2.set_xlim(-0.5, len(optimizer.history) + 0.5)

    return ax1, ax2


# Создаем анимацию
anim = FuncAnimation(fig, animate, frames=len(optimizer.history),
                     interval=800, repeat=False, blit=False)

plt.tight_layout()
plt.show()

# Статическая визуализация всех итераций
fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(15, 6))

# Статический график функции
ax3.plot(x_plot, y_plot, 'b-', linewidth=2, label='f(x)')
for j, step in enumerate(optimizer.history):
    color = colors[j]
    ax3.axvspan(step['a'], step['b'], alpha=0.2, color=color,
                label=f'Итер. {j}' if j % 3 == 0 else "")

ax3.plot(min_x, min_y, 'r*', markersize=15, label=f'Минимум: ({min_x:.4f}, {min_y:.4f})')
ax3.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax3.grid(True, alpha=0.3)
ax3.set_xlabel('x')
ax3.set_ylabel('f(x)')
ax3.set_title('Все итерации метода золотого сечения')
ax3.legend()

# График сходимости
iterations = [step['iteration'] for step in optimizer.history]
intervals = [step['interval_length'] for step in optimizer.history]
ax4.semilogy(iterations, intervals, 'bo-', linewidth=2, markersize=6)
ax4.grid(True, alpha=0.3)
ax4.set_xlabel('Итерация')
ax4.set_ylabel('Длина интервала (лог. шкала)')
ax4.set_title('Скорость сходимости метода')

plt.tight_layout()
plt.show()

# Выводим таблицу с результатами итераций
print("\nДетали итерационного процесса:")
print("Итер. |    a    |    b    |    y    |    z    |   f(y)  |   f(z)  | Длина инт.")
print("-" * 80)
for i, step in enumerate(optimizer.history[:10]):  # Показываем первые 10 итераций
    print(f"{step['iteration']:5} | {step['a']:7.4f} | {step['b']:7.4f} | "
          f"{step['y']:7.4f} | {step['z']:7.4f} | {step['f_y']:7.4f} | "
          f"{step['f_z']:7.4f} | {step['interval_length']:10.6f}")

if len(optimizer.history) > 10:
    print("... (показаны первые 10 из {} итераций)".format(len(optimizer.history)))

# Анализ эффективности
print(f"\nАнализ эффективности:")
print(f"Начальная длина интервала: {optimizer.history[0]['interval_length']:.6f}")
print(f"Финальная длина интервала: {optimizer.history[-1]['interval_length']:.6f}")
print(
    f"Коэффициент сокращения: {optimizer.history[0]['interval_length'] / optimizer.history[-1]['interval_length']:.2f}")
print(f"Теоретический коэффициент за n итераций: {(1 / optimizer.golden_ratio) ** len(optimizer.history):.2f}")