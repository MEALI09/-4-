# lab6_diff_variant4.py
# Python 3.8+
# Установи пакеты, если нужно:
# pip install numpy pandas matplotlib openpyxl xlsxwriter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os

# -------------------------
# Параметры задачи (вариант 4)
# -------------------------
def y_func(x):
    # y(x) = cos(pi * x^2 / 2)
    return np.cos(np.pi * x**2 / 2.0)

def y1_analytic(x):
    # y' = -pi * x * sin(pi x^2 / 2)
    return -np.pi * x * np.sin(np.pi * x**2 / 2.0)

def y2_analytic(x):
    # y'' = -pi * sin(pi x^2 /2) - pi^2 * x^2 * cos(pi x^2 / 2)
    return -np.pi * np.sin(np.pi * x**2 / 2.0) - (np.pi**2) * x**2 * np.cos(np.pi * x**2 / 2.0)

# -------------------------
# Численные формулы O(h^2)
# -------------------------
# центральные:
# y'_j ≈ (y_{j+1} - y_{j-1}) / (2h)
# y''_j ≈ (y_{j+1} - 2 y_j + y_{j-1}) / h^2
#
# односторонние (второго порядка) на границах:
# для j=0:
# y'_0 ≈ (-3 y0 + 4 y1 - y2) / (2h)
# y''_0 ≈ (2 y0 - 5 y1 + 4 y2 - y3) / h^2
# для j=n:
# y'_n ≈ (3 y_n - 4 y_{n-1} + y_{n-2}) / (2h)
# y''_n ≈ (2 y_n - 5 y_{n-1} + 4 y_{n-2} - y_{n-3}) / h^2

def numeric_derivatives(y_vals, h):
    n = len(y_vals) - 1
    y1_num = np.zeros(n+1)
    y2_num = np.zeros(n+1)

    # interior (central)
    for j in range(1, n):
        y1_num[j] = (y_vals[j+1] - y_vals[j-1]) / (2.0 * h)
        y2_num[j] = (y_vals[j+1] - 2.0*y_vals[j] + y_vals[j-1]) / (h*h)

    # boundaries — forward/backward formulas (2nd order)
    # j = 0
    if n >= 3:
        y1_num[0] = (-3.0*y_vals[0] + 4.0*y_vals[1] - y_vals[2]) / (2.0 * h)
        y2_num[0] = (2.0*y_vals[0] - 5.0*y_vals[1] + 4.0*y_vals[2] - y_vals[3]) / (h*h)
    else:
        # крайне малое n — fallback to one-sided first difference
        y1_num[0] = (y_vals[1] - y_vals[0]) / h
        y2_num[0] = 0.0

    # j = n
    if n >= 3:
        y1_num[n] = (3.0*y_vals[n] - 4.0*y_vals[n-1] + y_vals[n-2]) / (2.0 * h)
        y2_num[n] = (2.0*y_vals[n] - 5.0*y_vals[n-1] + 4.0*y_vals[n-2] - y_vals[n-3]) / (h*h)
    else:
        y1_num[n] = (y_vals[n] - y_vals[n-1]) / h
        y2_num[n] = 0.0

    return y1_num, y2_num

# -------------------------
# Основное: ввод n, расчёт, вывод, экспорт, график
# -------------------------
def main():
    print("Лабораторная: Численное дифференцирование — Вариант 4")
    # ввод n (20..100)
    while True:
        try:
            n = int(input("Введите n (число интервалов, 20..100, по умолчанию 50): ") or "50")
            if 20 <= n <= 100:
                break
            else:
                print("n должно быть в диапазоне 20..100")
        except ValueError:
            print("Введите целое число")

    h = 1.0 / n
    x = np.array([i * h for i in range(n+1)])   # x_j, j=0..n
    y = y_func(x)
    y1_exact = y1_analytic(x)
    y2_exact = y2_analytic(x)

    # численные производные
    y1_num, y2_num = numeric_derivatives(y, h)

    # ошибки
    err1 = np.abs(y1_exact - y1_num)
    err2 = np.abs(y2_exact - y2_num)

    # max errors and indices (first occurrence)
    idx_max_err1 = int(np.argmax(err1))
    idx_max_err2 = int(np.argmax(err2))
    max_err1 = err1[idx_max_err1]
    max_err2 = err2[idx_max_err2]

    # RMSE
    rmse1 = math.sqrt(np.mean((y1_exact - y1_num)**2))
    rmse2 = math.sqrt(np.mean((y2_exact - y2_num)**2))

    # вывод в консоль (кратко)
    print("\nРезультаты:")
    print(f"n = {n}, h = {h:.6e}")
    print(f"Max |err y'| = {max_err1:.6e} at j = {idx_max_err1}, x = {x[idx_max_err1]:.6f}")
    print(f"Max |err y''| = {max_err2:.6e} at j = {idx_max_err2}, x = {x[idx_max_err2]:.6f}")
    print(f"RMSE y'  = {rmse1:.6e}")
    print(f"RMSE y'' = {rmse2:.6e}")

    # Сохранение таблицы в Excel
    df = pd.DataFrame({
        "j": np.arange(n+1),
        "x": x,
        "y": y,
        "y'_exact": y1_exact,
        "y'_num": y1_num,
        "err_y'": err1,
        "y''_exact": y2_exact,
        "y''_num": y2_num,
        "err_y''": err2
    })

    summary = {
        "n": [n],
        "h": [h],
        "max_err_y'": [max_err1],
        "idx_max_err_y'": [idx_max_err1],
        "x_idx_max_err_y'": [x[idx_max_err1]],
        "rmse_y'": [rmse1],
        "max_err_y''": [max_err2],
        "idx_max_err_y''": [idx_max_err2],
        "x_idx_max_err_y''": [x[idx_max_err2]],
        "rmse_y''": [rmse2]
    }
    df_summary = pd.DataFrame(summary)

    excel_filename = "lab6_diff_variant4_results.xlsx"

    # Попытка сохранить и вставить график в Excel (используем xlsxwriter если он доступен)
    try:
        writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
        df.to_excel(writer, sheet_name="values", index=False)
        df_summary.to_excel(writer, sheet_name="summary", index=False)

        # Сохраняем график как png
        fig, axes = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
        # первая производная
        axes[0].plot(x, y1_exact, label="y' (точно)", color='blue')
        axes[0].plot(x, y1_num, label="y' (численно)", color='red', linestyle='--')
        axes[0].set_ylabel("y'")
        axes[0].legend()
        axes[0].grid(True)
        # вторая производная
        axes[1].plot(x, y2_exact, label="y'' (точно)", color='green')
        axes[1].plot(x, y2_num, label="y'' (численно)", color='orange', linestyle='--')
        axes[1].set_xlabel("x")
        axes[1].set_ylabel("y''")
        axes[1].legend()
        axes[1].grid(True)
        plt.suptitle("Численное дифференцирование — Вариант 4\n(точные и численные производные)")
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])

        png_name = "lab6_derivatives_variant4.png"
        fig.savefig(png_name, dpi=200)
        plt.close(fig)

        # вставляем картинку в новый лист
        workbook = writer.book
        worksheet = workbook.add_worksheet("plot")
        worksheet.insert_image('B2', png_name, {'x_scale': 0.9, 'y_scale': 0.9})
        # сохраняем
        writer.close()
        print(f"\n✅ Результаты и график сохранены в {excel_filename}")
        # оставить png файл рядом
    except Exception as e:
        # если не получилось с xlsxwriter — сохраняем просто CSV и PNG
        print("\n⚠️ Не получилось вставить картинку в Excel (попытка использовать xlsxwriter):", e)
        csv_name = "lab6_diff_values_variant4.csv"
        df.to_csv(csv_name, index=False)
        plt.figure(figsize=(8,6))
        plt.plot(x, y1_exact, label="y' (точно)")
        plt.plot(x, y1_num, '--', label="y' (численно)")
        plt.plot(x, y2_exact, label="y'' (точно)")
        plt.plot(x, y2_num, '--', label="y'' (численно)")
        plt.legend()
        plt.grid(True)
        png_name = "lab6_derivatives_variant4.png"
        plt.savefig(png_name, dpi=200)
        print(f"Сохранены: {csv_name} и {png_name}")

    # Вывод таблицы нескольких значимых узлов (для проверки) — печатаем первые 8 и последние 3
    pd.set_option('display.precision', 8)
    print("\nЧасть таблицы (первые 8 строк):")
    print(df.head(8).to_string(index=False))
    print("\n... (последние 3 строки):")
    print(df.tail(3).to_string(index=False))

if __name__ == "__main__":
    main()
