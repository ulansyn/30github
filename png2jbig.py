from PIL import Image, ImageFilter, ImageOps
import os
import subprocess
import shutil


def ultra_compress_avif(
        input_path: str,
        output_path: str,
        target_size_kb: int = 15,
        scale_factor: float = 0.3,
        avif_quality: int = 20,  # Качество AVIF (1-63, где 20 — баланс)
        threshold: int = 140  # Порог бинаризации
) -> None:
    """Сжимает мангу в AVIF (намного лучше WebP) до 5-15 KB без потери качества."""

    if not os.path.exists(input_path):
        print(f"Ошибка: Файл '{input_path}' не найден.")
        return

    try:
        with Image.open(input_path) as img:
            # Преобразуем в градации серого (8 бит вместо 24)
            img = img.convert("L")

            # Автоуровни для контраста
            img = ImageOps.autocontrast(img)

            # Уменьшаем разрешение
            new_size = (max(1, int(img.width * scale_factor)), max(1, int(img.height * scale_factor)))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Резкость для чёткости линий
            img = img.filter(ImageFilter.SHARPEN)

            # Бинаризация (чёрно-белое)
            img = img.point(lambda p: 255 if p > threshold else 0, mode="1")

            # Сохраняем во временный PNG (AVIF кодеры не поддерживают mode="1")
            temp_png = "temp_image.png"
            img.save(temp_png, format="PNG", optimize=True)

            # Проверяем наличие avifenc (AVIF-кодер)
            avifenc_path = shutil.which("avifenc")
            if not avifenc_path:
                print("Ошибка: avifenc не найден. Установите его из AOM или libavif.")
                return

            # Команда для avifenc (глубокая компрессия)
            subprocess.run([
                avifenc_path, temp_png, output_path,
                "--min", str(avif_quality),
                "--max", str(avif_quality),
                "--cq-level", str(avif_quality),
                "--speed", "8",
                "--jobs", "4"
            ], check=True)

            # Удаляем временный PNG
            os.remove(temp_png)

            final_size = os.path.getsize(output_path) / 1024  # KB

            print(f'Финальный размер AVIF: {final_size:.1f} KB')

            # Динамическое уменьшение качества, если размер превышает target_size_kb
            while final_size > target_size_kb and avif_quality < 63:
                avif_quality += 5
                subprocess.run([
                    avifenc_path, temp_png, output_path,
                    "--min", str(avif_quality),
                    "--max", str(avif_quality),
                    "--cq-level", str(avif_quality),
                    "--speed", "8",
                    "--jobs", "4"
                ], check=True)
                final_size = os.path.getsize(output_path) / 1024
                print(f'Уменьшено до {final_size:.1f} KB (качество {avif_quality})')

    except Exception as e:
        print(f'Ошибка: {e}')


# Запуск
if __name__ == "__main__":
    ultra_compress_avif(
        input_path="ффффффффффффффффффффффффффффффффф.png",
        output_path="compressed_manga.avif",
        target_size_kb=15,
        scale_factor=0.3,
        avif_quality=25,  # Можно уменьшить до 20 для еще меньшего размера
        threshold=150
    )
