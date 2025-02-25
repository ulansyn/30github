import segno
import io
from PIL import Image
import matplotlib.pyplot as plt

# Исходная ссылка (уже сокращённая, чтобы уместиться в микро QR-код)
url = "n9.cl/8f5x7"

try:
    # Создаем микро QR-код.
    qr = segno.make(url, micro=True)

    # Сохраняем QR-код в буфер как PNG.
    buffer = io.BytesIO()
    qr.save(buffer, kind='png', scale=10)  # scale=10 для увеличения размера изображения
    buffer.seek(0)

    # Открываем изображение с помощью PIL.
    img = Image.open(buffer)

    # Вывод изображения через системный просмотрщик.
    img.show()

    # Также выводим изображение внутри Python (например, если вы используете Jupyter Notebook).
    plt.figure(figsize=(4, 4))
    plt.imshow(img)
    plt.axis('off')
    plt.show()

except Exception as e:
    print("Не удалось создать QR-код:", e)
    