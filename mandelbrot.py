import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c, max_iter=100):
    """Вычисляет, принадлежит ли точка множеству Мандельброта."""
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z**2 + c
    return max_iter

def generate_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter=100):
    """Генерирует массив значений множества Мандельброта."""
    x_vals = np.linspace(xmin, xmax, width)
    y_vals = np.linspace(ymin, ymax, height)
    mandelbrot_set = np.zeros((height, width))

    for i, y in enumerate(y_vals):
        for j, x in enumerate(x_vals):
            mandelbrot_set[i, j] = mandelbrot(complex(x, y), max_iter)

    return mandelbrot_set

# Параметры для отрисовки
xmin, xmax, ymin, ymax = -2, 1, -1.5, 1.5
width, height = 1000, 1000
max_iter = 500

# Генерация множества Мандельброта
mandelbrot_image = generate_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter)

# Отображение множества
plt.figure(figsize=(10, 10))
plt.imshow(mandelbrot_image, extent=[xmin, xmax, ymin, ymax], cmap="inferno", interpolation="bilinear")
plt.colorbar(label="Iterations")
plt.title("Mandelbrot Set")
plt.xlabel("Real Part")
plt.ylabel("Imaginary Part")
plt.show()